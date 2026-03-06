from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize sentence transformer model"""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully")
    
    def create_embedding(self, text):
        """Create embedding for single text"""
        if isinstance(text, str):
            return self.model.encode(text, convert_to_numpy=True)
        return self.model.encode(str(text), convert_to_numpy=True)
    
    def create_embeddings_batch(self, texts):
        """Create embeddings for multiple texts"""
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

# Global instance
_embedder = None

def get_embedder():
    """Get or create global embedder instance"""
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder

def create_embedding(text):
    """Convenience function for single embedding"""
    return get_embedder().create_embedding(text)
