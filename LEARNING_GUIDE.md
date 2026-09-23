# RAG Learning Guide & Presentation Notes

This document provides a conceptual, step-by-step breakdown of each of the 6 tasks in the project. Use this guide to prepare for presentations, interviews, or explanations to peers.

---

## TASK 1 — RAG ENVIRONMENT SETUP & ARCHITECTURE

### What it is
The foundation of a RAG application: preparing the runtime environment, installing lightweight orchestration libraries, and establishing connections to three local services (PostgreSQL with pgvector, Redis, and Ollama).

### Why we use it
A production or local RAG pipeline consists of multiple moving parts. Instead of crashing unpredictably midway through execution, a dedicated environment script validates dependencies up front and provides actionable guidance if any service is down.

### How it works
1. Imports Python packages (`langchain`, `sentence_transformers`, `psycopg2`, `pgvector`, `redis`).
2. Tests TCP connectivity and database readiness for PostgreSQL and registers the `vector` extension.
3. Pings the local Redis server on port 6379.
4. Queries Ollama at `http://localhost:11434/api/tags` to ensure the local server is running and verifies whether the specified model (e.g., `llama3`) is installed. If not, it prints the exact `ollama pull` command.

### Where it is implemented
- [`task1_env_setup.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/task1_env_setup.py)
- [`config.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/config.py)
- [`db_utils.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/db_utils.py)

### What you should be able to explain in a presentation
- **LangChain**: Orchestrates the pipeline (retrieval + prompt + LLM).
- **HuggingFace**: Generates dense mathematical vectors locally on CPU/GPU without API keys.
- **PostgreSQL + pgvector**: Persists text chunks and performs vector similarity search.
- **Ollama**: Executes open-weights LLMs (`llama3`) locally with zero subscription cost and full privacy.
- **Redis**: In-memory database used as a high-speed semantic cache.

---

## TASK 2 — CHUNK SOURCE DOCUMENTS & GENERATE LOCAL EMBEDDINGS

### What it is
The document ingestion phase where raw, unstructured human text is broken down into small, digestible pieces (chunks) and converted into numerical vectors (embeddings).

### Why we use it
- **Context Limits**: Large language models cannot accept infinite context, and sending hundreds of pages degrades performance ("needle in a haystack" problem).
- **Semantic Resolution**: A single paragraph or concept is easier to match accurately than an entire 20-page document.
- **Semantic Search**: Text strings cannot be compared geometrically. Converting words into vectors captures meaning, allowing mathematical similarity comparison.

### How it works
1. **Load Document**: Read text from `data/documents.txt`.
2. **TextSplitter**: LangChain's `RecursiveCharacterTextSplitter` divides the text into chunks of 350 characters with a 50-character overlap (to preserve context across chunk boundaries).
3. **Embeddings**: The local `sentence-transformers/all-MiniLM-L6-v2` neural network converts each chunk into a 384-dimensional vector of real numbers.

### Where it is implemented
- [`task2_chunk_and_embed.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/task2_chunk_and_embed.py)
- [`data/documents.txt`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/data/documents.txt)

### What you should be able to explain in a presentation
- **Document vs. Chunk**: A document is the full raw file; a chunk is a specific, self-contained excerpt.
- **Why Chunk?**: Prevents LLM context overflow and focuses retrieval on only the exact relevant sentences.
- **What is an Embedding?**: A multi-dimensional coordinate vector representing the conceptual meaning of text.
- **Why Overlap?**: Overlap prevents key sentences or ideas from being cut in half at chunk boundaries.

---

## TASK 3 — STORE EMBEDDINGS WITH METADATA IN POSTGRESQL + PGVECTOR

### What it is
Storing processed chunks, their descriptive metadata, and their numerical embedding vectors in a PostgreSQL relational database powered by the `pgvector` extension.

### Why we use it
- Traditional relational databases only index and search exact strings, prefixes, or ranges.
- `pgvector` allows PostgreSQL to store vectors natively and perform nearest-neighbor searches directly inside SQL queries.
- Keeping metadata alongside vectors ensures traceability, source citations, and filtering capabilities.

### How it works
1. **Table Schema**:
   ```sql
   CREATE TABLE rag_documents (
       id SERIAL PRIMARY KEY,
       content TEXT NOT NULL,
       metadata JSONB,
       embedding vector(384)
   );
   ```
2. **Insertion**: Bulk inserts chunk text, JSON metadata (`source`, `chunk_index`), and 384-dim float arrays.
3. **Vector Similarity Search**: Uses the pgvector cosine distance operator `<=>`:
   ```sql
   SELECT id, content, metadata, 1 - (embedding <=> :query_vector) AS similarity
   FROM rag_documents
   ORDER BY embedding <=> :query_vector
   LIMIT 3;
   ```

### Where it is implemented
- [`task3_store_embeddings.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/task3_store_embeddings.py)

### What you should be able to explain in a presentation
- **pgvector**: An extension that gives PostgreSQL native vector storage and distance math.
- **Why Vector Databases**: They compare conceptual similarity in multi-dimensional space, unlike standard SQL `LIKE` or full-text search.
- **Metadata**: Contextual details (source file, paragraph index) stored with the vector to enable source attribution and document filtering.
- **Cosine Distance (`<=>`)**: Measures the angular difference between two vectors; distance = 0 means identical direction.

---

## TASK 4 — BUILD THE LANGCHAIN RETRIEVALQA RAG CHAIN

### What it is
The core RAG engine: combining information retrieval from pgvector with generative answer synthesis using a local LLM in Ollama.

### Why we use it
- Large language models do not know proprietary or updated private data, and frequently hallucinate plausible-sounding falsehoods.
- RAG "grounds" the model by injecting retrieved factual passages into the prompt, forcing the LLM to synthesize answers solely from verifiable facts.

### How it works
1. **User Question**: The user inputs a question (e.g., "What power source does Curiosity use?").
2. **Retriever**: Queries pgvector for the top $k=3$ most similar chunks.
3. **Prompt Augmentation**: Wraps the retrieved chunks into a strict system prompt:
   ```text
   Context: [Retrieved Chunks]
   Question: [User Question]
   Answer:
   ```
4. **Local LLM**: Passes the prompt to Ollama (`llama3`).
5. **Answer Generation**: The LLM reads the context and generates a precise, factual answer.

### Where it is implemented
- [`task4_retrieval_qa.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/task4_retrieval_qa.py)

### What you should be able to explain in a presentation
- **What is Retrieval**: Finding relevant snippets from an external database.
- **What is Augmentation**: Injecting those snippets into the LLM prompt.
- **What is Generation**: The LLM writing natural language answers from that context.
- **Why it stops hallucinations**: The prompt explicitly restricts the LLM to the provided context.

---

## TASK 5 — ADD REDIS SEMANTIC CACHE

### What it is
A high-performance caching layer in front of the RAG pipeline that checks if an incoming question is semantically identical to a previously answered question.

### Why we use it
- LLM inference is computationally expensive and slow (taking 2 to 10 seconds per response on local hardware).
- Traditional caches only work if the user types the exact identical character string.
- Semantic caching recognizes that "What powers Curiosity?" and "What is the energy source of Curiosity rover?" mean the exact same thing.

### How it works
1. When a user asks a question, compute its embedding vector with HuggingFace.
2. In Redis, iterate through cached questions and calculate cosine similarity between their vectors.
3. **If Similarity $\ge$ 0.88 (Cache HIT)**: Return the cached answer immediately from Redis in ~5 milliseconds. Bypasses pgvector and Ollama entirely.
4. **If Similarity $<$ 0.88 (Cache MISS)**: Call the Task 4 RAG pipeline, generate the answer, and store `{query, embedding, answer}` in Redis for future requests.

### Where it is implemented
- [`task5_redis_semantic_cache.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/task5_redis_semantic_cache.py)

### What you should be able to explain in a presentation
- **Exact vs. Semantic Cache**: Exact requires 100% character match; semantic matches conceptual meaning via vector similarity.
- **Performance Benefit**: Reduces response time from ~5000ms down to ~5ms for common questions.
- **Cost & Resource Savings**: Avoids redundant GPU/CPU consumption by skipping vector DB queries and LLM token generation.

---

## TASK 6 — EVALUATE RAG ANSWER QUALITY (10 TEST QUESTIONS)

### What it is
A structured, manual evaluation assessing whether our RAG system retrieves the correct information and generates faithful, non-hallucinated answers across exactly 10 test questions.

### Why we use it
- Without systematic evaluation, you cannot tell if changing chunk size, prompt templates, or embedding models improved or degraded answer quality.
- Evaluating both retrieval and answer generation independently pinpoints the exact component responsible for any error.

### How it works
1. Define **10 specific factual test questions** spanning the entire knowledge base.
2. For each question:
   - Retrieve top chunks from pgvector.
   - Generate answer using the RAG pipeline.
   - Inspect and record:
     - **Question**
     - **Retrieved Chunks**
     - **Generated Answer**
     - **Retrieval Relevance Score (1-5)**: Did the chunks contain the needed facts?
     - **Answer Faithfulness Score (1-5)**: Was the answer supported by the chunks without hallucination?
3. Compute average scores and export a Markdown report (`evaluation_report.md`).

### Where it is implemented
- [`task6_evaluate_rag.py`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/task6_evaluate_rag.py)
- [`evaluation_report.md`](file:///c:/Users/Admin/OneDrive%20-%20Agilisium%20Consulting%20India%20Private%20Limited/Desktop/RAG_7_Tasks/evaluation_report.md)

### What you should be able to explain in a presentation
- **The Two Failure Modes**:
  1. Retrieval failure: The right information was never provided to the model.
  2. Generation failure: The model had the information but fabricated false details.
- **Why Manual Evaluation Matters**: Provides transparent, interpretable ground truth verification without the opacity of automated black-box scoring.
