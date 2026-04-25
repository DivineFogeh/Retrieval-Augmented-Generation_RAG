# Part 2 – New Items and Cross-Corpus Query Results

## Part 2A – Targeted Queries (new items)

Collections queried: `wiki_new_items` | Top-k: 4

| Q# | Query | Top Sources (title · collection) | Scores | Answer (first 2 sentences) | Source origin |
|---|---|---|---|---|---|
| 1 | What is the difference between supervised and unsupervised learning? | Machine Learning (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Vector Database (wiki_new_items)<br>Neural Network (wiki_new_items) | 0.4037<br>0.7652<br>0.8026<br>0.8126 | In supervised learning, algorithms are trained on labeled datasets that include inputs paired with correct outputs. The algorithm learns to map inputs to outputs, and after training, can predict outpu | wiki_new_items |
| 2 | How does the transformer self-attention mechanism work? | Transformer (deep learning architecture) (wiki_new_items)<br>Neural Network (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Machine Learning (wiki_new_items) | 0.4150<br>0.7168<br>0.8497<br>0.8698 | The transformer self-attention mechanism works by computing three vectors for each token: a Query (Q), a Key (K), and a Value (V). Attention scores are calculated as the scaled dot product of Q and K, | wiki_new_items |
| 3 | What is Retrieval-Augmented Generation (RAG) and why is it useful? | Transformer (deep learning architecture) (wiki_new_items)<br>Vector Database (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Neural Network (wiki_new_items) | 0.7275<br>0.7677<br>0.8046<br>0.9070 | Retrieval-Augmented Generation (RAG) is a technique that combines a retrieval system with a generative language model. It first retrieves relevant documents from an external knowledge base and then co | wiki_new_items |
| 4 | How does Chroma store and search vector embeddings? | Vector Database (wiki_new_items)<br>Natural Language Processing (wiki_new_items)<br>Transformer (deep learning architecture) (wiki_new_items)<br>Neural Network (wiki_new_items) | 0.5319<br>0.6685<br>0.7472<br>0.8378 | Chroma is an open-source embedding database designed for use with LLMs. It provides a simple Python API for creating collections, adding documents with their embeddings and metadata, and querying by s | wiki_new_items |
| 5 | What activation functions are used in neural networks? | Neural Network (wiki_new_items)<br>Transformer (deep learning architecture) (wiki_new_items)<br>Machine Learning (wiki_new_items)<br>Natural Language Processing (wiki_new_items) | 0.2838<br>0.6119<br>0.6997<br>0.7339 | The activation functions used in neural networks include the sigmoid function, the hyperbolic tangent (tanh), and the rectified linear unit (ReLU). [Source 1: Neural Network – https://en.wikipedia.org | wiki_new_items |

## Part 2B – Cross-Corpus Queries

Collections queried: `wiki_starter`, `wiki_new_items` | Top-k: 4

| Q# | Query | Top Sources (title · collection) | Scores | Answer (first 2 sentences) | Source origin |
|---|---|---|---|---|---|
| 1 | How do machines learn from data? | Machine Learning (wiki_new_items)<br>Computer (wiki_starter)<br>Bioinformatics (wiki_starter)<br>Machine code (wiki_starter) | 0.4493<br>0.4942<br>0.5796<br>0.5847 | Machines learn from data by using algorithms to enable computers to imitate the way humans learn, gradually improving accuracy. This is done through the use of data and algorithms in machine learning, | wiki_new_items + wiki_starter |
| 2 | What is a neural network? | Neural Network (wiki_new_items)<br>Network (wiki_starter)<br>Neuron (wiki_starter)<br>Machine Learning (wiki_new_items) | 0.3087<br>0.4148<br>0.4961<br>0.5587 | A neural network is a computational model inspired by the structure and function of biological neural networks in the brain. It consists of layers of interconnected nodes (neurons) that process inform | wiki_new_items + wiki_starter |
| 3 | How does language understanding work in computers? | Language (wiki_starter)<br>Learning English (wiki_starter)<br>Linguistics (wiki_starter)<br>Programming language (wiki_starter) | 0.4334<br>0.5091<br>0.5193<br>0.5268 | I don't know based on the provided context. | wiki_starter |
| 4 | What is BERT and how was it trained? | Kermit the Frog (wiki_starter)<br>Piano (wiki_starter)<br>Turing test (wiki_starter)<br>George Carlin (wiki_starter) | 0.6869<br>0.7023<br>0.7035<br>0.7094 | I don't know based on the provided context. | wiki_starter |
| 5 | Explain the concept of overfitting in machine learning. | Machine Learning (wiki_new_items)<br>Computational complexity theory (wiki_starter)<br>Bioinformatics (wiki_starter)<br>Recognition (wiki_starter) | 0.5649<br>0.6545<br>0.7077<br>0.7157 | Overfitting is a common problem in machine learning where a model learns the training data too well, including its noise and outliers, and performs poorly on unseen data. Techniques to prevent overfit | wiki_new_items + wiki_starter |
