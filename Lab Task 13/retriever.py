
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import INDEX_PATH, TOP_K
import loader

_index = None
_model = None


def _get_index():
    global _index
    if _index is None:
        _index = faiss.read_index(str(INDEX_PATH))
    return _index


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def _embed(query):
    return _get_model().encode([query], convert_to_numpy=True).astype("float32")


def search(query: str, top_k: int = TOP_K) -> list:

    index  = _get_index()
    chunks = loader.load_chunks()

    distances, indices = index.search(_embed(query), k=top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(chunks):
            similarity = max(0.0, 1.0 - distances[0][i] / 2.0)
            results.append({**chunks[idx], "similarity": round(float(similarity), 4)})

    return results
