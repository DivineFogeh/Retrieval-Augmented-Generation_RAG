# ─── RAG Assignment 4 – Track A Configuration ───────────────────────────────

# Embedding model (same model used for both starter corpus and added items)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Vector DB
CHROMA_PATH       = "./chroma_text"
COLLECTION_WIKI   = "wiki_starter"      # Part 1 – starter Wikipedia corpus
COLLECTION_NEW    = "wiki_new_items"    # Part 2 – your own .txt files

# Retrieval
TOP_K = 4

# Starter corpus size  (5 000 – 20 000 per assignment spec)
STARTER_CORPUS_SIZE = 10_000

# ─── UTSA Llama 3.1 8B Generator Endpoint ────────────────────────────────────
UTSA_API_KEY   = "utsa-jABQlGLaTrae2bqMHyAvPxTvE9KTP0DEWYIXhvtgkDkVcGjp44rN6G56x1aGiyem"
UTSA_BASE_URL  = "http://149.165.173.247:8888/v1"
UTSA_MODEL     = "meta-llama/Llama-3.1-8B-Instruct"

# Generator settings
MAX_TOKENS     = 512
TEMPERATURE    = 0.1      # low temp → more faithful, grounded answers
