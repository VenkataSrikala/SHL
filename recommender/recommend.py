import faiss
import pandas as pd
import numpy as np
from embeddings.embedder import get_embedder
import os

class AssessmentRecommender:
    def __init__(self):
        """Initialize recommender with FAISS index and catalog"""
        print("Loading recommender...")
        
        # Load catalog
        self.df = pd.read_csv("data/processed/shl_catalog_clean.csv")
        
        # Load FAISS index
        if not os.path.exists("vector_db/index.faiss"):
            raise FileNotFoundError("FAISS index not found. Run build_embeddings.py first")
        
        self.index = faiss.read_index("vector_db/index.faiss")
        
        # Load embedder
        self.embedder = get_embedder()
        
        print(f"Loaded {len(self.df)} assessments")
        print(f"FAISS index size: {self.index.ntotal}")
    
    def recommend(self, query, k=10):
        """Recommend top-k assessments for query"""
        
        # Create query embedding
        query_vector = self.embedder.create_embedding(query)
        query_vector = query_vector.reshape(1, -1).astype('float32')
        
        # Search FAISS index
        distances, indices = self.index.search(query_vector, k)
        
        # Build results
        results = []
        for idx in indices[0]:
            if idx < len(self.df):
                row = self.df.iloc[idx]
                results.append({
                    "name": row["name"],
                    "url": row["url"],
                    "description": row["description"],
                    "duration": int(row["duration"]) if pd.notna(row["duration"]) else None,
                    "test_type": [row["test_type"]],
                    "remote_support": row["remote_support"],
                    "adaptive_support": row["adaptive_support"]
                })
        
        return results
    
    def recommend_balanced(self, query, k=10):
        """Recommend with balanced test types"""
        
        # Get more candidates
        candidates = self.recommend(query, k=k*3)
        
        # Balance by test type
        balanced = []
        test_types = {}
        
        for assessment in candidates:
            test_type = assessment["test_type"][0]
            count = test_types.get(test_type, 0)
            
            # Limit per category
            if count < k // 2:
                balanced.append(assessment)
                test_types[test_type] = count + 1
            
            if len(balanced) >= k:
                break
        
        # Fill remaining slots if needed
        if len(balanced) < k:
            for assessment in candidates:
                if assessment not in balanced:
                    balanced.append(assessment)
                if len(balanced) >= k:
                    break
        
        return balanced[:k]

# Global instance
_recommender = None

def get_recommender():
    """Get or create global recommender instance"""
    global _recommender
    if _recommender is None:
        _recommender = AssessmentRecommender()
    return _recommender

def recommend_assessments(query, k=10, balanced=True):
    """Convenience function for recommendations"""
    recommender = get_recommender()
    if balanced:
        return recommender.recommend_balanced(query, k)
    return recommender.recommend(query, k)
