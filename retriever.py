"""
retriever.py – Track A Text RAG
Embeds a query with all-MiniLM-L6-v2 and returns top-k chunks from a
Chroma collection together with their metadata and distance scores.
"""

from __future__ import annotations
from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_PATH, TOP_K, EMBEDDING_MODEL


# ── module-level singletons (loaded once) ────────────────────────────────────
_model: SentenceTransformer | None = None
_client: chromadb.PersistentClient | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"[retriever] loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


# ── public API ────────────────────────────────────────────────────────────────

def retrieve(
    query: str,
    collection_name: str,
    top_k: int = TOP_K,
) -> List[Dict[str, Any]]:
    """
    Embed *query* and return the top-k most similar chunks from *collection_name*.

    Each result dict contains:
        id        – Chroma document id
        document  – raw text of the chunk
        metadata  – dict with 'title' and 'url'
        score     – cosine distance (lower = more similar)
    """
    model  = _get_model()
    client = _get_client()

    embedding = model.encode(query).tolist()

    try:
        col = client.get_collection(collection_name)
    except Exception:
        raise ValueError(
            f"Collection '{collection_name}' not found in '{CHROMA_PATH}'. "
            "Run the ingest script first."
        )

    results = col.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist, rid in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
        results["ids"][0],
    ):
        hits.append({"id": rid, "document": doc, "metadata": meta, "score": dist})

    return hits


def retrieve_multi(
    query: str,
    collection_names: List[str],
    top_k: int = TOP_K,
) -> List[Dict[str, Any]]:
    """
    Query multiple collections and return the globally top-k results
    sorted by score (ascending distance = most relevant first).
    """
    all_hits: List[Dict[str, Any]] = []
    for name in collection_names:
        try:
            hits = retrieve(query, name, top_k=top_k)
            for h in hits:
                h["collection"] = name
            all_hits.extend(hits)
        except ValueError:
            pass  # collection not yet populated – skip silently

    all_hits.sort(key=lambda h: h["score"])
    return all_hits[:top_k]


if __name__ == "__main__":
    # quick smoke-test
    from config import COLLECTION_WIKI
    q = "What is photosynthesis?"
    print(f"Query: {q}\n")
    for r in retrieve(q, COLLECTION_WIKI):
        print(f"  [{r['score']:.4f}] {r['metadata'].get('title')} – {r['metadata'].get('url')}")
        print(f"  {r['document'][:120]}\n")
