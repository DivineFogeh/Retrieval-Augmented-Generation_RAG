# Assignment 4 – Track A: Text RAG
**Course:** CS 6263 – LLM and Agentic Systems  
**Track:** A – Text RAG (Short)

---

## Track Declaration

**Track A – Text RAG.**  
Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (no API key required).  
Starter corpus: `wikimedia/wikipedia` (20231101.simple), 10,000 passages.  
Generator: UTSA-hosted Llama 3.1 8B Instruct (`meta-llama/Llama-3.1-8B-Instruct`).  
Vector DB: ChromaDB (persistent client, cosine similarity).

---

## Pipeline Summary

The pipeline follows the standard RAG architecture with three modules:

**Retriever** (`retriever.py`): A query string is encoded with `all-MiniLM-L6-v2` (384-dimensional embeddings) into a query vector. ChromaDB performs approximate nearest-neighbour search (HNSW with cosine distance) against the stored passage embeddings and returns the top-k (k=4) chunks with their metadata (title, URL) and similarity scores.

**Generator** (`generator.py`): The retrieved chunks are assembled into a grounded prompt using the format specified in the assignment (numbered context passages with title and URL). The system prompt instructs the model to answer *only* from the provided context and to cite sources. The prompt is sent to the UTSA Llama 3.1 8B endpoint via its OpenAI-compatible `/v1/chat/completions` API.

**Evaluation Driver** (`run_part1.py`, `run_part2.py`): Each script iterates over a list of queries, calls the retriever and generator, and writes a Markdown results table to the `results/` directory.

The Part 1 starter corpus is populated by `ingest.py`, which streams the Simple English Wikipedia dataset, truncates passages to 512 characters, embeds in batches of 256, and inserts into a persistent Chroma collection. Part 2 custom `.txt` files are ingested similarly in `run_part2.py`.

---

## Hugging Face Resources Used

| Resource | Purpose |
|---|---|
| `wikimedia/wikipedia` (20231101.simple) | Starter text corpus (no Cohere API key needed) |
| `sentence-transformers/all-MiniLM-L6-v2` | Embedding model for both corpus and queries |

---

## Part 1 Results

Corpus: `wiki_starter` | Top-k: 4

| Q# | Query | Top Sources (title · url) | Similarity Scores | Generated Answer (first 2 sentences) | Grounded? |
|---|---|---|---|---|---|
| 1 | What is photosynthesis and how does it work? | Photosynthesis · https://simple.wikipedia.org/wiki/Photosynthesis<br>Chlorophyll · https://simple.wikipedia.org/wiki/Chlorophyll<br>Chloroplast · https://simple.wikipedia.org/wiki/Chloroplast<br>Carbon dioxide · https://simple.wikipedia.org/wiki/Carbon%20dioxide | 0.2483<br>0.4176<br>0.4180<br>0.4860 | Photosynthesis is how plants and some microorganisms make carbohydrates. It is an endothermic (takes in heat) chemical process which uses sunlight to turn carbon dioxide into sugars. | Yes |
| 2 | How does the human immune system fight infections? | Pathogen · https://simple.wikipedia.org/wiki/Pathogen<br>Immunology · https://simple.wikipedia.org/wiki/Immunology<br>Immunity (medical) · https://simple.wikipedia.org/wiki/Immunity%20%28medical%29<br>Vaccination · https://simple.wikipedia.org/wiki/Vaccination | 0.3673<br>0.3773<br>0.4216<br>0.4695 | The human immune system fights infections in two main types: innate immunity and adaptive immunity. Innate immunity protects the host against infection but has no 'memory', and so gives no long-term immunity. | Yes |
| 3 | What caused the French Revolution? | French Revolution · https://simple.wikipedia.org/wiki/French%20Revolution<br>Napoleonic Wars · https://simple.wikipedia.org/wiki/Napoleonic%20Wars<br>1830 · https://simple.wikipedia.org/wiki/1830<br>1680s · https://simple.wikipedia.org/wiki/1680s | 0.3134<br>0.4707<br>0.4815<br>0.5280 | The French Revolution was caused by many different things, including the Age of Enlightenment, which brought new ideas on how the government should work, and France's debt. | Yes |
| 4 | Explain the theory of natural selection. | Evolution · https://simple.wikipedia.org/wiki/Evolution<br>Eugenics · https://simple.wikipedia.org/wiki/Eugenics<br>Charles Darwin · https://simple.wikipedia.org/wiki/Charles%20Darwin<br>Evolutionary biology · https://simple.wikipedia.org/wiki/Evolutionary%20biology | 0.4782<br>0.5206<br>0.5913<br>0.5997 | I don't know based on the provided context. | No — retrieved passages were truncated and did not contain a direct explanation of natural selection |
| 5 | What is the water cycle? | Water cycle · https://simple.wikipedia.org/wiki/Water%20cycle<br>Cycle · https://simple.wikipedia.org/wiki/Cycle<br>Drought · https://simple.wikipedia.org/wiki/Drought<br>Water vapor · https://simple.wikipedia.org/wiki/Water%20vapor | 0.1819<br>0.4834<br>0.5183<br>0.5298 | The water cycle is the cycle that water goes through on Earth. It is essential for life as we know it. | Yes |
| 6 | How do black holes form? | Black hole · https://simple.wikipedia.org/wiki/Black%20hole<br>Fecund universes · https://simple.wikipedia.org/wiki/Fecund%20universes<br>Neutron star · https://simple.wikipedia.org/wiki/Neutron%20star<br>Stellar evolution · https://simple.wikipedia.org/wiki/Stellar%20evolution | 0.4626<br>0.5347<br>0.6563<br>0.6694 | According to the general theory of relativity, a black hole starts existing when spacetime gets curved by a huge mass. | Yes |
| 7 | What is the difference between DNA and RNA? | RNA · https://simple.wikipedia.org/wiki/RNA<br>Nucleotide · https://simple.wikipedia.org/wiki/Nucleotide<br>DNA · https://simple.wikipedia.org/wiki/DNA<br>Gene · https://simple.wikipedia.org/wiki/Gene | 0.3314<br>0.3841<br>0.4463<br>0.5042 | DNA and RNA are physically different. DNA has two intercoiled strands, but RNA only has one strand. | Yes |
| 8 | What were the main causes of World War I? | World War · https://simple.wikipedia.org/wiki/World%20War<br>1914 · https://simple.wikipedia.org/wiki/1914<br>Cold War · https://simple.wikipedia.org/wiki/Cold%20War<br>Axis powers · https://simple.wikipedia.org/wiki/Axis%20powers | 0.4690<br>0.5139<br>0.5667<br>0.5716 | I don't know based on the provided context. | No — retrieved chunks were about general war history, not WWI causes specifically |
| 9 | How does a computer processor work? | Central processing unit · https://simple.wikipedia.org/wiki/Central_processing_unit<br>Microprocessor · https://simple.wikipedia.org/wiki/Microprocessor<br>Computer program · https://simple.wikipedia.org/wiki/Computer%20program<br>Multithreading · https://simple.wikipedia.org/wiki/Multithreading | 0.2758<br>0.4012<br>0.4243<br>0.4676 | A computer processor, specifically a central processing unit (CPU), works by sending signals to control other parts of the computer. It reads a list of instructions, called a computer program, and runs them. | Yes |
| 10 | What is quantum mechanics? | Quantum mechanics · https://simple.wikipedia.org/wiki/Quantum%20mechanics<br>Schrödinger equation · https://simple.wikipedia.org/wiki/Schr%C3%B6dinger%20equation<br>Quantum entanglement · https://simple.wikipedia.org/wiki/Quantum%20entanglement<br>Classical mechanics · https://simple.wikipedia.org/wiki/Classical%20mechanics | 0.2965<br>0.4547<br>0.4664<br>0.4666 | Quantum mechanics explains how the universe works at a scale smaller than atoms. It is also called quantum physics or quantum theory. | Yes |

---

## Part 2 Results

### Part 2A – Targeted Queries (new items only)

Collections queried: `wiki_new_items` | Top-k: 4

| Q# | Query | Top Sources (title · collection) | Scores | Answer (first 2 sentences) | Source origin |
|---|---|---|---|---|---|
| 1 | What is the difference between supervised and unsupervised learning? | Machine Learning (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Vector Database (wiki_new_items)<br>Neural Network (wiki_new_items) | 0.4037<br>0.7652<br>0.8026<br>0.8126 | In supervised learning, algorithms are trained on labeled datasets that include inputs paired with correct outputs. The algorithm learns to map inputs to outputs, and after training, can predict outputs for new, unseen inputs. | wiki_new_items |
| 2 | How does the transformer self-attention mechanism work? | Transformer (deep learning architecture) (wiki_new_items)<br>Neural Network (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Machine Learning (wiki_new_items) | 0.4150<br>0.7168<br>0.8497<br>0.8698 | The transformer self-attention mechanism works by computing three vectors for each token: a Query (Q), a Key (K), and a Value (V). Attention scores are calculated as the scaled dot product of Q and K, normalized with a softmax. | wiki_new_items |
| 3 | What is Retrieval-Augmented Generation (RAG) and why is it useful? | Transformer (deep learning architecture) (wiki_new_items)<br>Vector Database (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Neural Network (wiki_new_items) | 0.7275<br>0.7677<br>0.8046<br>0.9070 | Retrieval-Augmented Generation (RAG) is a technique that combines a retrieval system with a generative language model. It first retrieves relevant documents from an external knowledge base and then conditions the generator on these documents to produce a grounded answer. | wiki_new_items |
| 4 | How does Chroma store and search vector embeddings? | Vector Database (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Transformer (deep learning architecture) (wiki_new_items)<br>Neural Network (wiki_new_items) | 0.5319<br>0.6685<br>0.7472<br>0.8378 | Chroma is an open-source embedding database designed for use with LLMs. It provides a simple Python API for creating collections, adding documents with their embeddings and metadata, and querying by similarity. | wiki_new_items |
| 5 | What activation functions are used in neural networks? | Neural Network (wiki_new_items)<br>Transformer (deep learning architecture) (wiki_new_items)<br>Machine Learning (wiki_new_items)<br>Natural Language Processing (wiki_new_items) | 0.2838<br>0.6119<br>0.6997<br>0.7339 | The activation functions used in neural networks include the sigmoid function, the hyperbolic tangent (tanh), and the rectified linear unit (ReLU). ReLU has become the most widely used activation function in deep networks due to its simplicity and effectiveness. | wiki_new_items |

### Part 2B – Cross-Corpus Queries

Collections queried: `wiki_starter`, `wiki_new_items` | Top-k: 4

| Q# | Query | Top Sources (title · collection) | Scores | Answer (first 2 sentences) | Source origin |
|---|---|---|---|---|---|
| 1 | How do machines learn from data? | Machine Learning (wiki_new_items)<br>Computer (wiki_starter)<br>Bioinformatics (wiki_starter)<br>Machine code (wiki_starter) | 0.4493<br>0.4942<br>0.5796<br>0.5847 | Machines learn from data by using algorithms to enable computers to imitate the way humans learn, gradually improving accuracy. This is done through the use of data and algorithms in machine learning, a branch of artificial intelligence. | wiki_new_items + wiki_starter |
| 2 | What is a neural network? | Neural Network (wiki_new_items)<br>Network (wiki_starter)<br>Neuron (wiki_starter)<br>Machine Learning (wiki_new_items) | 0.3087<br>0.4148<br>0.4961<br>0.5587 | A neural network is a computational model inspired by the structure and function of biological neural networks in the brain. It consists of layers of interconnected nodes (neurons) that process information using connectionist approaches. | wiki_new_items + wiki_starter |
| 3 | How does language understanding work in computers? | Language (wiki_starter)<br>Learning English (wiki_starter)<br>Linguistics (wiki_starter)<br>Programming language (wiki_starter) | 0.4334<br>0.5091<br>0.5193<br>0.5268 | I don't know based on the provided context. | wiki_starter only |
| 4 | What is BERT and how was it trained? | Kermit the Frog (wiki_starter)<br>Piano (wiki_starter)<br>Turing test (wiki_starter)<br>George Carlin (wiki_starter) | 0.6869<br>0.7023<br>0.7035<br>0.7094 | I don't know based on the provided context. | wiki_starter only |
| 5 | Explain the concept of overfitting in machine learning. | Machine Learning (wiki_new_items)<br>Computational complexity theory (wiki_starter)<br>Bioinformatics (wiki_starter)<br>Recognition (wiki_starter) | 0.5649<br>0.6545<br>0.7077<br>0.7157 | Overfitting is a common problem in machine learning where a model learns the training data too well, including its noise and outliers, and performs poorly on unseen data. Techniques to prevent overfitting include regularization, dropout, and early stopping. | wiki_new_items + wiki_starter |

---

## Reflection

### When did retrieval succeed, and when did it return topically similar but not actually useful chunks?

Retrieval worked well for queries with precise, distinctive terminology. Queries like "What is photosynthesis?" (score 0.25), "What is quantum mechanics?" (score 0.30), and "What is the difference between DNA and RNA?" (score 0.33) all retrieved the correct top article with low cosine distance and produced grounded, accurate answers. The `all-MiniLM-L6-v2` embeddings captured semantic similarity effectively for well-covered Simple English Wikipedia topics.

Retrieval was less reliable for two queries: Q4 ("Explain the theory of natural selection") and Q8 ("What were the main causes of World War I?"). Both retrieved topically adjacent articles — Evolution, Charles Darwin, and Eugenics for Q4; World War, 1914, and Cold War for Q8 — but none of the retrieved passages contained a direct, detailed explanation of the target concept. The generator correctly responded "I don't know based on the provided context" rather than hallucinating, which demonstrates the grounding prompt working as intended. The root cause is that passages were truncated to 512 characters, so detailed explanatory content was often cut off.

### What happened when you ran cross-corpus queries?

Cross-corpus queries produced a clear pattern. Queries using general language ("How do machines learn?", "What is a neural network?", "Explain overfitting") correctly mixed chunks from both `wiki_starter` and `wiki_new_items`, with the new AI/ML files ranking as the top source due to their richer detail on those topics. However, Q3 ("How does language understanding work in computers?") and Q4 ("What is BERT and how was it trained?") retrieved entirely from `wiki_starter` — and notably Q4 returned completely irrelevant results (Kermit the Frog, Piano) because "BERT" as an NLP model does not appear in Simple English Wikipedia at all. The embedding model had no relevant vector to pull from either collection for that specific query, demonstrating a hard limitation of dense retrieval when a concept is entirely absent from the corpus.

### What is one thing you would change about the pipeline if you had another day?

The most impactful improvement would be **chunk-level splitting**: currently each Wikipedia article and custom file is stored as a single document truncated to 512 characters. A proper chunking strategy — splitting into overlapping windows of ~200 tokens with 50-token overlap — would allow finer-grained retrieval and reduce the chance that useful content is lost beyond the truncation cutoff (as seen in Q4 and Q8). A secondary improvement would be adding a **reranker** (e.g., a cross-encoder like `cross-encoder/ms-marco-MiniLM-L-6-v2`) as a second-stage filter on the top-20 ANN candidates, which typically improves precision significantly at modest latency cost.

---

## Repository Structure

```
rag_assignment/
├── .gitignore
├── config.py           # all hyperparameters and endpoint config
├── retriever.py        # embed query → top-k Chroma results
├── generator.py        # grounded prompt → Llama 3.1 8B answer
├── ingest.py           # populate starter Wikipedia corpus
├── run_part1.py        # Part 1: 10 baseline queries
├── run_part2.py        # Part 2: ingest new items + 10 queries
├── requirements.txt
├── README.md
├── REPORT.md           # this file
├── data/               # custom .txt files (Part 2 new items)
│   ├── machine_learning.txt
│   ├── neural_networks.txt
│   ├── natural_language_processing.txt
│   ├── vector_databases.txt
│   └── transformer_architecture.txt
└── results/            # generated after running scripts
    ├── part1_results.md
    └── part2_results.md
```

## How to Reproduce

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Populate starter corpus (~10,000 Wikipedia passages, ~5 min on CPU)
python ingest.py

# 3. Run Part 1 baseline queries
python run_part1.py

# 4. Ingest new items and run Part 2 queries
python run_part2.py
```
