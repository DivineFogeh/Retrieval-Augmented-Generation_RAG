"""
run_part2.py – Track A Text RAG  ·  Part 2: New Items + Cross-Corpus Queries
1. Ingests the 5 custom .txt files under data/ into a separate Chroma collection.
2. Runs 5 targeted queries (expected to retrieve from the new items).
3. Runs 5 cross-corpus queries (may retrieve from either collection).
Writes results to results/part2_results.md

Usage:
    python run_part2.py
"""

from __future__ import annotations
import os, glob

import chromadb
from sentence_transformers import SentenceTransformer

from retriever import retrieve, retrieve_multi
from generator import generate
from config import (
    CHROMA_PATH,
    COLLECTION_WIKI,
    COLLECTION_NEW,
    EMBEDDING_MODEL,
    TOP_K,
)

os.makedirs("results", exist_ok=True)

# ── Step 1: ingest custom .txt files ─────────────────────────────────────────

def ingest_new_items() -> int:
    print("[part2] Loading embedding model …")
    model  = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # idempotent: drop and recreate
    try:
        client.delete_collection(COLLECTION_NEW)
    except Exception:
        pass
    col = client.create_collection(
        name=COLLECTION_NEW,
        metadata={"hnsw:space": "cosine"},
    )

    txt_files = sorted(glob.glob("data/*.txt"))
    if not txt_files:
        raise FileNotFoundError("No .txt files found under data/")

    ids, texts, metadatas = [], [], []
    for fpath in txt_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # parse optional title/url lines at the top
        lines  = content.splitlines()
        title  = lines[0].replace("Title:", "").strip() if lines[0].startswith("Title:") else os.path.basename(fpath)
        url    = lines[1].replace("URL:", "").strip()   if len(lines) > 1 and lines[1].startswith("URL:") else fpath

        ids.append(os.path.basename(fpath))
        texts.append(content)
        metadatas.append({"title": title, "url": url})
        print(f"  + {os.path.basename(fpath):40s} → '{title}'")

    embs = model.encode(texts, show_progress_bar=True).tolist()
    col.add(ids=ids, embeddings=embs, documents=texts, metadatas=metadatas)
    print(f"[part2] Ingested {len(ids)} new items into '{COLLECTION_NEW}'.\n")
    return len(ids)


# ── Queries ───────────────────────────────────────────────────────────────────

# 5 targeted queries → should retrieve from the new AI/ML files
TARGETED_QUERIES = [
    "What is the difference between supervised and unsupervised learning?",
    "How does the transformer self-attention mechanism work?",
    "What is Retrieval-Augmented Generation (RAG) and why is it useful?",
    "How does Chroma store and search vector embeddings?",
    "What activation functions are used in neural networks?",
]

# 5 cross-corpus queries → may pull from both Wikipedia starter AND new items
CROSS_QUERIES = [
    "How do machines learn from data?",
    "What is a neural network?",
    "How does language understanding work in computers?",
    "What is BERT and how was it trained?",
    "Explain the concept of overfitting in machine learning.",
]


def truncate(text: str, n: int = 120) -> str:
    return text[:n].replace("\n", " ") + ("…" if len(text) > n else "")


def run_queries(queries, collections, label: str):
    rows = []
    for qid, query in enumerate(queries, 1):
        print(f"\n  [{qid}/{len(queries)}] {query}")
        chunks = retrieve_multi(query, collections, top_k=TOP_K)
        answer = generate(query, chunks)
        sentences = answer.split(". ")
        answer_short = ". ".join(sentences[:2]).strip()
        if not answer_short.endswith("."):
            answer_short += "."

        # tag each chunk with which collection it came from
        for c in chunks:
            if "collection" not in c:
                c["collection"] = "?"

        rows.append({
            "qid": qid, "query": query,
            "chunks": chunks, "answer": answer_short,
        })
        print(f"    Collections hit: {[c['collection'] for c in chunks]}")
        print(f"    Answer: {answer_short[:120]}")
    return rows


def rows_to_markdown(rows, label, collections_queried):
    lines = [
        f"## {label}\n",
        f"Collections queried: `{'`, `'.join(collections_queried)}` | Top-k: {TOP_K}\n",
        "| Q# | Query | Top Sources (title · collection) | Scores | Answer (first 2 sentences) | Source origin |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        q      = r["query"].replace("|", "\\|")
        srcs   = "<br>".join(
            f"{c['metadata'].get('title','?')} ({c['collection']})"
            for c in r["chunks"]
        )
        scores = "<br>".join(f"{c['score']:.4f}" for c in r["chunks"])
        ans    = r["answer"].replace("|", "\\|")[:200]
        origins = set(c["collection"] for c in r["chunks"])
        origin_str = " + ".join(sorted(origins))
        lines.append(f"| {r['qid']} | {q} | {srcs} | {scores} | {ans} | {origin_str} |")
    return "\n".join(lines)


def run_part2() -> None:
    ingest_new_items()

    collections_both = [COLLECTION_WIKI, COLLECTION_NEW]

    print("\n─── Targeted Queries (new items only) ───")
    targeted_rows = run_queries(TARGETED_QUERIES, [COLLECTION_NEW], "Targeted")

    print("\n─── Cross-Corpus Queries (both collections) ───")
    cross_rows = run_queries(CROSS_QUERIES, collections_both, "Cross-Corpus")

    md_targeted = rows_to_markdown(targeted_rows, "Part 2A – Targeted Queries (new items)", [COLLECTION_NEW])
    md_cross    = rows_to_markdown(cross_rows,    "Part 2B – Cross-Corpus Queries",          collections_both)

    out = "# Part 2 – New Items and Cross-Corpus Query Results\n\n" + md_targeted + "\n\n" + md_cross + "\n"
    out_path = "results/part2_results.md"
    with open(out_path, "w") as f:
        f.write(out)
    print(f"\n[part2] Results saved to {out_path}")


if __name__ == "__main__":
    run_part2()
