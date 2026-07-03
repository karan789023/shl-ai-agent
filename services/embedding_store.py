import numpy as np
from services.embeddings import get_model


def build_and_save_embeddings(catalog, path="data/processed/embeddings.npy"):
    model = get_model()

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

    embeddings = np.array(embeddings).astype("float32")
    np.save(path, embeddings)

    return embeddings


def load_embeddings(path="data/processed/embeddings.npy"):
    return np.load(path)