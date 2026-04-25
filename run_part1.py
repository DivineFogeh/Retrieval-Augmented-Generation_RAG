"""
run_part1.py – Track A Text RAG  ·  Part 1: Baseline Queries
Queries the starter Wikipedia corpus (10 queries) and writes a results
table to results/part1_results.md  (and prints to stdout).

Usage:
    python run_part1.py
"""

from __future__ import annotations
import os, textwrap

from retriever import retrieve
from generator import generate
from config import COLLECTION_WIKI, TOP_K

os.makedirs("results", exist_ok=True)

# ── 10 baseline queries ───────────────────────────────────────────────────────
QUERIES = [
    "What is photosynthesis and how does it work?",
    "How does the human immune system fight infections?",
    "What caused the French Revolution?",
    "Explain the theory of natural selection.",
    "What is the water cycle?",
    "How do black holes form?",
    "What is the difference between DNA and RNA?",
    "What were the main causes of World War I?",
    "How does a computer processor work?",
    "What is quantum mechanics?",
]


def truncate(text: str, n: int = 100) -> str:
    return text[:n].replace("\n", " ") + ("…" if len(text) > n else "")


def run_part1() -> None:
    rows = []

    for qid, query in enumerate(QUERIES, 1):
        print(f"\n[{qid:02d}/{len(QUERIES)}] {query}")

        chunks = retrieve(query, COLLECTION_WIKI, top_k=TOP_K)
        answer = generate(query, chunks)

        # First two sentences of the answer
        sentences = answer.split(". ")
        answer_short = ". ".join(sentences[:2]).strip()
        if not answer_short.endswith("."):
            answer_short += "."

        # Grounded judgment heuristic: does the answer reference any title?
        titles = [c["metadata"].get("title", "") for c in chunks]
        urls   = [c["metadata"].get("url", "") for c in chunks]
        grounded = any(t.lower()[:10] in answer.lower() for t in titles if t)

        rows.append({
            "qid":     qid,
            "query":   query,
            "chunks":  chunks,
            "answer":  answer_short,
            "grounded": "Yes" if grounded else "Manual check",
        })

        print(f"  Sources: {[c['metadata'].get('title','?') for c in chunks]}")
        print(f"  Answer : {answer_short[:120]}")

    # ── write markdown table ──────────────────────────────────────────────────
    lines = [
        "# Part 1 – Baseline Query Results\n",
        f"Corpus: `{COLLECTION_WIKI}` | Top-k: {TOP_K}\n",
        "| Q# | Query | Top Sources (title · url) | Similarity Scores | Generated Answer (first 2 sentences) | Grounded? |",
        "|---|---|---|---|---|---|",
    ]

    for r in rows:
        q      = r["query"].replace("|", "\\|")
        srcs   = "<br>".join(
            f"{c['metadata'].get('title','?')} · {c['metadata'].get('url','?')}"
            for c in r["chunks"]
        )
        scores = "<br>".join(f"{c['score']:.4f}" for c in r["chunks"])
        ans    = r["answer"].replace("|", "\\|")[:200]
        lines.append(f"| {r['qid']} | {q} | {srcs} | {scores} | {ans} | {r['grounded']} |")

    table = "\n".join(lines)
    print("\n\n" + table)

    out_path = "results/part1_results.md"
    with open(out_path, "w") as f:
        f.write(table + "\n")
    print(f"\n[part1] Results saved to {out_path}")


if __name__ == "__main__":
    run_part1()
