"""
Vector retrieval service.
Computes cosine similarity between query embeddings and stored chunk embeddings.
"""

from typing import Any
import numpy as np

from app.config import settings
from app.database import get_db
from app.llm import call_embedding_query


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two 1D vectors."""
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


async def search_chunks(
    query: str,
    subject: str | None = None,
    user_id: str | None = None,
    top_k: int = 4,
    min_score: float = 0.3,
) -> list[dict[str, Any]]:
    """
    Given a search query, embeds it and ranks stored chunks by cosine similarity.
    Returns top_k chunks with their metadata and similarity score.
    """
    user_id = user_id or settings.default_user_id
    db = get_db()

    # 1. Embed query using query-specific embedding
    query_vector = await call_embedding_query(query)
    query_vec = np.array(query_vector, dtype=np.float32)

    # 2. Build MongoDB query filter
    mongo_filter: dict[str, Any] = {"user_id": user_id}
    if subject and subject.strip() and subject.lower() != "all":
        mongo_filter["subject"] = {"$regex": f"^{subject.strip()}$", "$options": "i"}

    # 3. Fetch candidate chunks (text + metadata + embedding)
    cursor = db.chunks.find(
        mongo_filter,
        {"embedding": 1, "text": 1, "filename": 1, "page": 1, "subject": 1, "note_id": 1},
    )
    chunks = await cursor.to_list(length=1000)

    if not chunks:
        return []

    # 4. Compute similarities
    scored_chunks: list[dict[str, Any]] = []
    for c in chunks:
        if "embedding" not in c or not c["embedding"]:
            continue
        c_vec = np.array(c["embedding"], dtype=np.float32)
        # Guardrail: skip chunk if dimensions do not match active model
        if c_vec.shape != query_vec.shape:
            continue

        score = cosine_similarity(query_vec, c_vec)
        if score >= min_score:
            scored_chunks.append({
                "chunk_id": str(c["_id"]),
                "note_id": c.get("note_id", ""),
                "filename": c.get("filename", ""),
                "page": c.get("page", 1),
                "subject": c.get("subject", "General"),
                "text": c.get("text", ""),
                "score": round(score, 4),
            })

    # 5. Sort descending by score and pick top_k
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]
