import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = BASE_DIR / "data" / "processed" / "catalog.json"


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
from services.embeddings import get_embedding, embed_catalog
from services.embedding_store import build_and_save_embeddings, load_embeddings
from services.faiss_store import FaissStore
from services.bm25 import BM25Retriever
import numpy as np


class Retriever:
    def __init__(self, catalog, use_saved=True):

        self.catalog = catalog

        # BM25
        self.bm25 = BM25Retriever(catalog)

        # Embeddings
        if use_saved:
            self.embeddings = load_embeddings()
        else:
            self.embeddings = build_and_save_embeddings(catalog)

        # FAISS
        dim = self.embeddings.shape[1]
        self.faiss = FaissStore(dim)
        self.faiss.add(self.embeddings, catalog)

    def search(self, query, top_k=5):

        # FAISS results (semantic)
        query_vec = get_embedding(query)
        faiss_results = self.faiss.search(query_vec, top_k)

        # BM25 results (keyword)
        bm25_results = self.bm25.search(query, top_k)

        # 🔥 HYBRID SCORING (REAL UPGRADE)
        score_map = {}

        # FAISS weight = 0.7
        for item, score in faiss_results:
            key = item["name"]
            score_map[key] = score_map.get(key, 0) + (0.7 * score)

        # BM25 weight = 0.3
        for item, score in bm25_results:
            key = item["name"]
            score_map[key] = score_map.get(key, 0) + (0.3 * score)

        # FINAL SORTING
        final = sorted(
            self.catalog,
            key=lambda x: score_map.get(x["name"], 0),
            reverse=True
        )

        return final[:top_k]