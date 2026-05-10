"""Retrieval-augmented generation helpers."""

from functools import lru_cache
from pathlib import Path
from typing import TypedDict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"


class KnowledgeSearchResult(TypedDict):
    """A retrieved knowledge note and its vector distance."""

    source: str
    content: str
    distance: float


class KnowledgeIndex(TypedDict):
    """Loaded knowledge notes and their FAISS index."""

    texts: list[str]
    sources: list[str]
    index: faiss.IndexFlatL2 | None


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load the embedding model only when RAG search is used."""
    try:
        return SentenceTransformer(MODEL_NAME, local_files_only=True)
    except Exception:
        return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def get_knowledge_index() -> KnowledgeIndex:
    """Load knowledge notes and build the vector index on first use."""
    knowledge_texts: list[str] = []
    knowledge_sources: list[str] = []

    for file_path in sorted(KNOWLEDGE_DIR.iterdir()):
        if file_path.suffix.lower() not in {".md", ".txt"}:
            continue

        knowledge_texts.append(file_path.read_text(encoding="utf-8"))
        knowledge_sources.append(file_path.name)

    if not knowledge_texts:
        return {"texts": [], "sources": [], "index": None}

    embeddings = np.asarray(get_model().encode(knowledge_texts), dtype="float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return {"texts": knowledge_texts, "sources": knowledge_sources, "index": index}


def search_knowledge(query: str, top_k: int = 2) -> list[KnowledgeSearchResult]:
    """Search knowledge notes related to the user query."""
    knowledge_index = get_knowledge_index()
    knowledge_texts = knowledge_index["texts"]
    knowledge_sources = knowledge_index["sources"]
    index = knowledge_index["index"]

    if not query.strip() or not knowledge_texts or index is None:
        return []

    limited_top_k = min(top_k, len(knowledge_texts))
    query_embedding = np.asarray(get_model().encode([query]), dtype="float32")
    distances, indices = index.search(query_embedding, limited_top_k)

    results: list[KnowledgeSearchResult] = []
    for distance, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        results.append(
            {
                "source": knowledge_sources[idx],
                "content": knowledge_texts[idx],
                "distance": float(distance),
            }
        )

    return results
