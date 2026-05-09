"""Retrieval-augmented generation helpers."""

from pathlib import Path
from typing import TypedDict

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"


class KnowledgeSearchResult(TypedDict):
    """A retrieved knowledge note and its vector distance."""

    source: str
    content: str
    distance: float


model = SentenceTransformer(MODEL_NAME)

knowledge_texts: list[str] = []
knowledge_sources: list[str] = []

for file_path in sorted(KNOWLEDGE_DIR.iterdir()):
    if file_path.suffix.lower() not in {".md", ".txt"}:
        continue

    knowledge_texts.append(file_path.read_text(encoding="utf-8"))
    knowledge_sources.append(file_path.name)

if knowledge_texts:
    embeddings = model.encode(knowledge_texts)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
else:
    embeddings = None
    index = None


def search_knowledge(query: str, top_k: int = 2) -> list[KnowledgeSearchResult]:
    """Search knowledge notes related to the user query."""
    if not query.strip() or not knowledge_texts or index is None:
        return []

    limited_top_k = min(top_k, len(knowledge_texts))
    query_embedding = model.encode([query])
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
