# RAG Learning Project — Complete 6-Task Implementation

A clean, beginner-friendly **Retrieval-Augmented Generation (RAG)** learning project designed strictly for presentation and practical understanding.

The system runs **completely locally** without paid or external API keys, using local HuggingFace embeddings and a local Ollama LLM.

---

## 1. What the Project Does

This project demonstrates the complete end-to-end architecture of a local RAG system:
1. **Splits** raw documents into semantically coherent chunks using LangChain.
2. **Encodes** chunks into 384-dimensional dense vectors using a local HuggingFace model (`all-MiniLM-L6-v2`).
3. **Stores** the chunks, metadata, and vectors in **PostgreSQL + pgvector** and performs vector similarity search via cosine distance (`<=>`).
4. **Builds a LangChain RetrievalQA chain** to query pgvector and feed relevant context to a local **Ollama LLM** (`llama3`), generating grounded answers.
5. **Integrates a Redis Semantic Cache** in front of the RAG pipeline to intercept repeated or semantically equivalent questions, returning instant cached answers and saving LLM compute.
6. **Evaluates Answer Quality** across **exactly 10 test questions**, tracking chunk retrieval relevance, answer faithfulness, and hallucination prevention.

---

## 2. Technologies Used

| Technology | Role in Project | Why Used |
| :--- | :--- | :--- |
| **LangChain** | Pipeline Orchestration | Manages text splitters, prompt templates, and RetrievalQA |
| **HuggingFace** | Dense Vector Embeddings | `all-MiniLM-L6-v2` runs locally; no API keys or costs |
| **PostgreSQL + pgvector** | Vector Database | Stores chunk texts, JSON metadata, and vector embeddings |
| **Ollama** | Local LLM Engine | Runs open-source models (`llama3`, `mistral`) completely on local CPU/GPU |
| **Redis** | Semantic Caching | In-memory key-value store calculating similarity for rapid query caching |
| **Python 3.12** | Core Programming Language | Clean scripting environment with modular task files |

---

## 3. Prerequisites

- **Python 3.12+** installed.
- **PostgreSQL** with the `pgvector` extension installed.
- **Redis** server installed.
- **Ollama** installed with your chosen model (e.g., `llama3`).

---

## 4. Installation

1. **Open a terminal** inside the project folder:
   ```bash
   cd "RAG_7_Tasks"
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure environment variables**:
   Copy `.env.example` to `.env` and adjust database/Redis passwords if different from default:
   ```bash
   copy .env.example .env
   ```

---

## 5. How to Start PostgreSQL / pgvector

1. **Verify or start the PostgreSQL service**:
   - **Windows Services**: Open `services.msc`, locate `postgresql-x64-<version>`, and click **Start**.
   - **Command Line**:
     ```powershell
     net start postgresql-x64-16
     ```
2. **Ensure pgvector is enabled**:
   The scripts will automatically attempt to execute:
   ```sql
   CREATE DATABASE rag_db;
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
   If pgvector is not installed, download the pre-compiled binary or installer for your PostgreSQL version from [pgvector GitHub releases](https://github.com/pgvector/pgvector).

---

## 6. How to Start Redis

- **Windows Native / MSI**:
  - Start the service in `services.msc` (`Redis`) or run `redis-server.exe` in your terminal.
- **WSL (Windows Subsystem for Linux)**:
  ```bash
  wsl sudo service redis-server start
  ```
- Default port: `6379`.

---

## 7. How to Start Ollama and Pull the Model

1. **Download and install Ollama** from [ollama.com](https://ollama.com).
2. **Start the Ollama background service**:
   - Launch the Ollama Desktop app, or run:
     ```bash
     ollama serve
     ```
3. **Pull the required model**:
   ```bash
   ollama pull llama3
   ```
   *(If you prefer a lighter model, run `ollama pull phi3` or `ollama pull mistral` and update `OLLAMA_MODEL` in `config.py`)*.

---

## 8. How to Run the Project

You can run individual tasks or execute the entire pipeline with the interactive menu:

### Interactive Menu Runner
```bash
python main.py
```

### Individual Task Scripts
- **Task 1: Environment Diagnostics**
  ```bash
  python task1_env_setup.py
  ```
- **Task 2: Chunk Documents & Local Embeddings**
  ```bash
  python task2_chunk_and_embed.py
  ```
- **Task 3: Store in PostgreSQL + pgvector**
  ```bash
  python task3_store_embeddings.py
  ```
- **Task 4: LangChain RetrievalQA Chain**
  ```bash
  python task4_retrieval_qa.py
  ```
- **Task 5: Redis Semantic Cache Layer**
  ```bash
  python task5_redis_semantic_cache.py
  ```
- **Task 6: 10-Question Evaluation**
  ```bash
  python task6_evaluate_rag.py
  ```

---

## 9. How the RAG Pipeline Works

### Ingestion Flow (Tasks 2 & 3)
```text
Source Document (data/documents.txt)
       ↓
LangChain RecursiveCharacterTextSplitter (chunk_size=350, overlap=50)
       ↓
Text Chunks + Metadata (source, chunk_index)
       ↓
Local HuggingFace Model (all-MiniLM-L6-v2)
       ↓
384-dimensional Embeddings
       ↓
PostgreSQL + pgvector (rag_documents table)
```

### Query & Cache Flow (Tasks 4 & 5)
```text
User Question
      ↓
Redis Semantic Cache
      ↓
┌─────────────────────────────────┐
│ Cosine similarity >= 0.88 with  │
│ an existing cached question?    │
└────────────────┬────────────────┘
        Yes      │       No
         ┌───────┴───────┐
         ↓               ↓
   [CACHE HIT]     [CACHE MISS]
   Return answer   Embed query with HuggingFace
   in ~5ms               ↓
                   pgvector Cosine Distance Search (<=>)
                         ↓
                   Top-K Relevant Chunks
                         ↓
                   LangChain Grounded Prompt ({context} + {question})
                         ↓
                   Local Ollama LLM (llama3)
                         ↓
                   Generated Answer
                         ↓
                   Save Query + Vector + Answer to Redis
```

---

## 10. How to Run the 10-Question Evaluation

Run:
```bash
python task6_evaluate_rag.py
```

### Evaluation Output
The script tests **exactly 10 domain questions** against the Mars exploration dataset and records:
1. **Question**: Exact user query.
2. **Retrieved Chunks**: Passages retrieved by pgvector.
3. **Generated Answer**: Response synthesized by Ollama.
4. **Manual Relevance Score**:
   - **Retrieval Score (1 to 5)**: Verifies whether the retrieved chunks contained the required facts.
   - **Faithfulness Score (1 to 5)**: Verifies whether the generated answer accurately reflects the chunks without hallucination.

The results are displayed in an ASCII summary table and exported to `evaluation_report.md`.
