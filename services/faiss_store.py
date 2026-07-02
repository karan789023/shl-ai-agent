import faiss
import numpy as np


class FaissStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)  # INNER PRODUCT = cosine (after normalize)
        self.items = []

    def add(self, embeddings, items):
        embeddings = self.normalize(embeddings)
        self.index.add(embeddings)
        self.items = items

    def search(self, query_embedding, top_k=5):
        query_embedding = self.normalize([query_embedding])

        D, I = self.index.search(query_embedding, top_k)

        results = []
        scores = D[0]

        for idx, score in zip(I[0], scores):
            if idx < len(self.items):
                results.append((self.items[idx], float(score)))

        return results

    def normalize(self, x):
        x = np.array(x).astype("float32")
        faiss.normalize_L2(x)
        return x