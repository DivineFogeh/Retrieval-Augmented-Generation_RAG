# Assignment 4 – RAG System | CS 6263

**Track: A – Text RAG (Short)**

## Datasets and Models Used

| Component | Resource |
|---|---|
| Starter corpus | `wikipedia/wikipedia` (config: `20220301.simple`) |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector database | ChromaDB (persistent, cosine similarity) |
| Generator | UTSA Llama 3.1 8B Instruct (`meta-llama/Llama-3.1-8B-Instruct`) |

## Quick Start

```bash
pip install -r requirements.txt
python ingest.py          # populate starter corpus (~10 000 passages)
python run_part1.py       # Part 1: 10 baseline queries
python run_part2.py       # Part 2: new items + cross-corpus queries
```

## Repository Structure

| File/Dir | Description |
|---|---|
| `config.py` | Embedding model, generator endpoint, top-k, paths |
| `retriever.py` | Query embedding + ChromaDB ANN search |
| `generator.py` | Grounded prompt assembly + Llama API call |
| `ingest.py` | Populates Wikipedia starter corpus in ChromaDB |
| `run_part1.py` | Runs 10 Part 1 queries, writes `results/part1_results.md` |
| `run_part2.py` | Ingests new items, runs 10 Part 2 queries, writes `results/part2_results.md` |
| `data/` | 5 custom Wikipedia-style .txt files on AI/ML topics |
| `results/` | Generated result tables (created at runtime) |
| `chroma_text/` | Persisted vector DB (created by ingest.py) |
| `REPORT.md` | Full report with pipeline summary, results, and reflection |
