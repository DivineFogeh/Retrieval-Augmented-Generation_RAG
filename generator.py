"""
generator.py – Track A Text RAG
Assembles a grounded prompt from retrieved chunks and calls the
UTSA-hosted Llama 3.1 8B endpoint via the OpenAI-compatible API.
"""

from __future__ import annotations
from typing import List, Dict, Any

from openai import OpenAI

from config import (
    UTSA_API_KEY,
    UTSA_BASE_URL,
    UTSA_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
)

# ── client singleton ──────────────────────────────────────────────────────────
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=UTSA_API_KEY, base_url=UTSA_BASE_URL)
    return _client


# ── prompt assembly ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Answer the user's question using ONLY the provided context passages. "
    "If the context does not contain enough information to answer, say 'I don't know based on the provided context.' "
    "Always cite your sources at the end of your answer using the format: "
    "[Source N: <title> – <url>]"
)


def _build_context_block(chunks: List[Dict[str, Any]]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, 1):
        title = chunk["metadata"].get("title", "Unknown")
        url   = chunk["metadata"].get("url",   "N/A")
        text  = chunk["document"]
        lines.append(f"[{i}] title: {title}, url: {url}\n{text}")
    return "\n\n".join(lines)


def _build_user_message(query: str, chunks: List[Dict[str, Any]]) -> str:
    context = _build_context_block(chunks)
    return (
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )


# ── public API ────────────────────────────────────────────────────────────────

def generate(
    query: str,
    chunks: List[Dict[str, Any]],
) -> str:
    """
    Given a user *query* and a list of retrieved *chunks*, call the Llama
    endpoint and return the generated answer string.
    """
    client       = _get_client()
    user_message = _build_user_message(query, chunks)

    response = client.chat.completions.create(
        model=UTSA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    # quick smoke-test (requires collection to be populated first)
    from retriever import retrieve
    from config import COLLECTION_WIKI

    q      = "What is photosynthesis?"
    chunks = retrieve(q, COLLECTION_WIKI)
    answer = generate(q, chunks)
    print(f"Q: {q}\n\nA: {answer}")
