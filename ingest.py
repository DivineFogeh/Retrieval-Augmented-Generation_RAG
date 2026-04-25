"""
ingest.py – Track A Text RAG
Populates the Chroma starter corpus from the wikipedia/wikipedia
(20220301.simple) dataset using sentence-transformers all-MiniLM-L6-v2.
This avoids any Cohere API key requirement.

Run once before run_part1.py:
    python ingest.py
"""

from __future__ import annotations
import sys
import textwrap

import chromadb
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_PATH,
    COLLECTION_WIKI,
    EMBEDDING_MODEL,
    STARTER_CORPUS_SIZE,
)

BATCH_SIZE   = 256
MAX_CHAR_LEN = 512   # truncate very long passages to keep embeddings fast


def chunk_text(text: str, max_len: int = MAX_CHAR_LEN) -> str:
    """Return the first max_len characters of a passage."""
    return text[:max_len].strip()


def ingest_wikipedia(limit: int = STARTER_CORPUS_SIZE) -> None:
    print(f"[ingest] Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"[ingest] Connecting to Chroma at: {CHROMA_PATH}")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Drop and recreate so re-runs are idempotent
    try:
        client.delete_collection(COLLECTION_WIKI)
        print(f"[ingest] Dropped existing collection '{COLLECTION_WIKI}'")
    except Exception:
        pass
    col = client.create_collection(
        name=COLLECTION_WIKI,
        metadata={"hnsw:space": "cosine"},
    )

    print(f"[ingest] Streaming wikimedia/wikipedia (20231101.simple), target {limit:,} passages …")
    ds = load_dataset(
        "wikimedia/wikipedia",
        "20231101.simple",
        split="train",
        streaming=True,
    )

    ids, texts, embeddings, metadatas = [], [], [], []
    total = 0

    for i, row in enumerate(ds):
        if total >= limit:
            break

        title   = row.get("title", "")
        url     = row.get("url", "")
        content = chunk_text(row.get("text", ""))
        if not content:
            continue

        ids.append(str(i))
        texts.append(content)
        metadatas.append({"title": title, "url": url})
        total += 1

        if len(ids) == BATCH_SIZE:
            embs = model.encode(texts, show_progress_bar=False).tolist()
            col.add(ids=ids, embeddings=embs, documents=texts, metadatas=metadatas)
            ids, texts, embeddings, metadatas = [], [], [], []
            print(f"  … ingested {total:,} / {limit:,}", end="\r", flush=True)

    # flush remainder
    if ids:
        embs = model.encode(texts, show_progress_bar=False).tolist()
        col.add(ids=ids, embeddings=embs, documents=texts, metadatas=metadatas)

    print(f"\n[ingest] Done. {total:,} passages stored in collection '{COLLECTION_WIKI}'.")


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else STARTER_CORPUS_SIZE
    ingest_wikipedia(limit)