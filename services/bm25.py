from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self, catalog):
        self.catalog = catalog
        self.tokenized = []

        for item in catalog:
            text = (
                item.get("name", "") + " " +
                item.get("description", "") + " " +
                " ".join(item.get("skills", [])) + " " +
                item.get("category", "")
            )
            self.tokenized.append(text.lower().split())

        self.bm25 = BM25Okapi(self.tokenized)

    def search(self, query, top_k=5):
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for idx, score in ranked[:top_k]:
            results.append((self.catalog[idx], float(score)))

        return results