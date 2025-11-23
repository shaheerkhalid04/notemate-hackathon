import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import pickle
import os

class RAGEngine:
    def __init__(self, db_path: str = "./vector_db"):
        self.db_path = db_path
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        self.index = None
        self.documents = []
        self.collection_name = None
        
        os.makedirs(db_path, exist_ok=True)
        
    def create_collection(self, collection_name: str):
        self.collection_name = collection_name
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        return True
    
    def add_documents(self, collection_name: str, chunks: List[str]):
        if not chunks:
            return
            
        # Generate embeddings
        embeddings = self.embedder.encode(chunks)
        
        # Add to Faiss index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents
        self.documents.extend(chunks)
        
        # Save to disk
        self._save_collection()
        
    def query(self, collection_name: str, query_text: str, n_results: int = 3) -> List[str]:
        if not self.index or not self.documents:
            return []
            
        # Generate query embedding
        query_embedding = self.embedder.encode([query_text])
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), n_results)
        
        # Return documents
        results = []
        for idx in indices[0]:
            if idx < len(self.documents) and idx >= 0:
                results.append(self.documents[idx])
                
        return results
    
    def _save_collection(self):
        if self.index and self.documents and self.collection_name:
            # Save index
            faiss.write_index(self.index, f"{self.db_path}/{self.collection_name}_index.faiss")
            # Save documents
            with open(f"{self.db_path}/{self.collection_name}_docs.pkl", 'wb') as f:
                pickle.dump(self.documents, f)
    
    def _load_collection(self, collection_name: str):
        try:
            # Load index
            self.index = faiss.read_index(f"{self.db_path}/{collection_name}_index.faiss")
            # Load documents
            with open(f"{self.db_path}/{collection_name}_docs.pkl", 'rb') as f:
                self.documents = pickle.load(f)
            self.collection_name = collection_name
            return True
        except:
            return False