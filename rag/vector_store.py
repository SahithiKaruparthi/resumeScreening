import os
import json
import chromadb
from chromadb.utils import embedding_functions
from rag.embeddings import EmbeddingManager
import config

class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Wrap initialization in try/except to handle Streamlit's file watcher issues
        try:
            # Initialize embedding function
            self.embedding_manager = EmbeddingManager()
            
            # Initialize ChromaDB client
            os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
            self.client = chromadb.PersistentClient(path=config.VECTOR_DB_PATH)
            
            # Get or create collection for roles
            self.roles_collection = self.client.get_or_create_collection(
                name="roles_collection",
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name=config.EMBEDDING_MODEL
                )
            )
            self._initialized = True
        except RuntimeError as e:
            print(f"Error initializing VectorStore: {e}")
            # Set placeholder attributes that will be reinitialized on next access
            self.embedding_manager = None
            self.client = None
            self.roles_collection = None
            self._initialized = False
    
    def _ensure_initialized(self):
        """Make sure the class is properly initialized before use"""
        if not self._initialized:
            self.__init__()
            if not self._initialized:
                raise RuntimeError("Failed to initialize VectorStore")
            
    def calculate_similarity_score(self, resume_text, role_id):
        """Calculate the similarity score between a resume and a role's requirements."""
        try:
            role_requirements = self.get_role_requirements(role_id)
            
            if not role_requirements:
                print(f"No requirements found for role ID: {role_id}")
                return 0.0  # No requirements found
            
            # Calculate similarity using the vector store
            results = self.query_similar(resume_text, n_results=1)
            
            # Debugging: Print the results structure
            print(f"Query results: {results}")
            
            if not results or not results.get("distances") or not results["distances"][0]:
                print(f"No similarity results found for role ID: {role_id}")
                return 0.0
            
            # Convert distance to similarity
            similarity_score = 1 - results["distances"][0][0]
            return similarity_score
        except Exception as e:
            print(f"Error calculating similarity score: {e}")
            return 0.0
    
    def add_role(self, role_id, role_title, role_requirements):
        """Add a role to the vector store"""
        self._ensure_initialized()
        
        try:
            # Add document to collection
            self.roles_collection.add(
                documents=[role_requirements],
                metadatas=[{"role_id": str(role_id), "title": role_title}],
                ids=[f"role_{role_id}"]
            )
            return True
        except Exception as e:
            print(f"Error adding role to vector store: {e}")
            return False
    
    def update_role(self, role_id, role_title, role_requirements):
        """Update a role in the vector store"""
        self._ensure_initialized()
        
        try:
            # Update document in collection
            self.roles_collection.update(
                documents=[role_requirements],
                metadatas=[{"role_id": str(role_id), "title": role_title}],
                ids=[f"role_{role_id}"]
            )
            return True
        except Exception as e:
            print(f"Error updating role in vector store: {e}")
            return False
    
    def delete_role(self, role_id):
        """Delete a role from the vector store"""
        self._ensure_initialized()
        
        try:
            # Delete document from collection
            self.roles_collection.delete(ids=[f"role_{role_id}"])
            return True
        except Exception as e:
            print(f"Error deleting role from vector store: {e}")
            return False
    
    def query_similar(self, query_text, n_results=5):
        """Query the vector store for similar role requirements"""
        self._ensure_initialized()
        
        try:
            results = self.roles_collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error querying vector store: {e}")
            return {"ids": [[]], "distances": [[]], "metadatas": [[]], "documents": [[]]}
    
    def get_role_requirements(self, role_id):
        """Get the requirements for a specific role"""
        self._ensure_initialized()
        
        try:
            result = self.roles_collection.get(ids=[f"role_{role_id}"])
            if result and result['documents']:
                return result['documents'][0]
            return None
        except Exception as e:
            print(f"Error retrieving role requirements: {e}")
            return None