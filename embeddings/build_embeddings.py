import pandas as pd
import faiss
import numpy as np
from embedder import Embedder
import os

def build_faiss_index():
    """Build FAISS index from processed catalog"""
    print("Building FAISS index...")
    
    # Load processed data
    df = pd.read_csv("data/processed/shl_catalog_clean.csv")
    print(f"Loaded {len(df)} assessments")
    
    # Initialize embedder
    embedder = Embedder()
    
    # Create embeddings
    texts = df['combined_text'].tolist()
    embeddings = embedder.create_embeddings_batch(texts)
    
    print(f"Created embeddings with shape: {embeddings.shape}")
    
    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    # Save index
    os.makedirs("vector_db", exist_ok=True)
    faiss.write_index(index, "vector_db/index.faiss")
    
    print(f"FAISS index created with {index.ntotal} vectors")
    print("Saved to vector_db/index.faiss")
    
    return index

if __name__ == "__main__":
    build_faiss_index()
