from sentence_transformers import SentenceTransformer

# Lightweight but powerful model
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Convert text into vector (embedding)
    """
    return model.encode(text)


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