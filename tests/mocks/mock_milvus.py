# tests/mocks/mock_milvus.py
import numpy as np

# ====== MOCK MILVUS C0LLECTION ======
class MockMilvusConnection:
    # Set up 
    def __init__(self):
        self.vectors = []
        self.metadata = []

    # Insert
    def insert(self, vectors, metadatas):
        self.vectors.extend(vectors)
        self.metadata.extend(metadatas)

    # Search
    def search(self, query_vector, top_k=3):
        if not self.vectors:
            return []
        dists = [np.linalg.norm(np.array(v) - np.array(query_vector)) for v in self.vectors]
        top_indices = np.argsort(dists)[:top_k]
        return [(self.metadata[i], dists[i]) for i in top_indices]