from functools import lru_cache

@lru_cache()
def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    model = get_model()
    return model.encode(text).tolist()

def embed_catalog(catalog):
    """
    Convert full catalog into embeddings
    """
    texts = []

    for item in catalog:
        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("skills", [])) + " " +
            item.get("category", "")
        )
        texts.append(text)

    embeddings = model.encode(texts, show_progress_bar=True)

    return embeddings