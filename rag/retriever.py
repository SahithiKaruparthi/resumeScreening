from rag.vector_store import VectorStore
from rag.embeddings import EmbeddingManager
import numpy as np

class RagRetriever:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_manager = EmbeddingManager()
    
    def initialize_from_db(self, roles):
        """Initialize vector store from database roles"""
        for role in roles:
            self.vector_store.add_role(
                role_id=role.id,
                role_title=role.title,
                role_requirements=role.requirements
            )
            
    def get_role_requirements(self, role_id):
        """Get requirements text for a specific role"""
        return self.vector_store.get_role_requirements(role_id)
    
    def calculate_resume_similarity(self, resume_text, role_id):
        """Calculate similarity between resume and role requirements"""
        # Get role requirements
        requirements = self.vector_store.get_role_requirements(role_id)
        if not requirements:
            return 0.0
            
        # Get embeddings
        resume_embedding = self.embedding_manager.get_embedding(resume_text)
        requirements_embedding = self.embedding_manager.get_embedding(requirements)
        
        # Calculate similarity
        similarity = self.embedding_manager.compute_similarity(resume_embedding, requirements_embedding)
        
        return float(similarity)