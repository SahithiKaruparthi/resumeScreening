from sentence_transformers import SentenceTransformer
import numpy as np
import config

class EmbeddingManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls)
            cls._instance.model = SentenceTransformer(config.EMBEDDING_MODEL)
        return cls._instance
    
    def get_embedding(self, text):
        """Get embedding for a single text"""
        if not text:
            return None
        return self.model.encode(text)
    
    def get_embeddings(self, texts):
        """Get embeddings for a list of texts"""
        if not texts:
            return []
        return self.model.encode(texts)

    def compute_similarity(self, embedding1, embedding2):
        """Compute cosine similarity between two embeddings"""
        if embedding1 is None or embedding2 is None:
            return 0.0
            
        # Normalize vectors
        norm_emb1 = embedding1 / np.linalg.norm(embedding1)
        norm_emb2 = embedding2 / np.linalg.norm(embedding2)
        
        # Compute cosine similarity
        return np.dot(norm_emb1, norm_emb2)