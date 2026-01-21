import faiss
import pickle
import os
import numpy as np

VECTOR_STORE_PATH = "data/vectorstore/index.faiss"
METADATA_PATH = "data/vectorstore/metadata.pkl"

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = [] # List of dicts corresponding to vectors
        
    def create_index(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        
    def add_documents(self, embeddings: list, documents: list):
        """
        embeddings: List of numpy arrays or a numpy array of shape (n, d)
        documents: List of metadata dicts or text content strings
        """
        if self.index is None:
            raise ValueError("Index not initialized. Call create_index first.")
            
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(documents)
        
    def search(self, query_vector, k: int = 3):
        if self.index is None or self.index.ntotal == 0:
            return []
            
        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "metadata": self.metadata[idx],
                    "score": float(distances[0][i])
                })
        return results

    def save(self):
        os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
        if self.index:
            faiss.write_index(self.index, VECTOR_STORE_PATH)
        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)
            
    def load(self):
        if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(METADATA_PATH):
            self.index = faiss.read_index(VECTOR_STORE_PATH)
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)
            return True
        return False
        
vector_store = VectorStore()
