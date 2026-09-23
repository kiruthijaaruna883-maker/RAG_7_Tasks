"""TASK 1: RAG Environment Setup and Service Diagnostics.

Purpose:
Project setup + vector database and local service diagnostics.

This script:
1. Explains what each core component does in the RAG architecture.
2. Verifies installed Python libraries.
3. Tests connectivity to PostgreSQL, pgvector, Redis, and Ollama.
4. If an Ollama model is missing, displays the exact command to pull it.
"""

import sys
import config
from db_utils import (
    ensure_postgres_database,
    check_redis_connection,
    check_ollama_connection,
)


def print_component_explanations():
    """Explains what each required component does in beginner-friendly terms."""
    print("=" * 75)
    print(" TASK 1: RAG ENVIRONMENT SETUP & ARCHITECTURE COMPONENTS")
    print("=" * 75)
    print("""
1. LangChain:
   - What it does: An open-source orchestration framework for LLM applications.
   - In this project: Glues together document loading, text splitting, vector
     retrieval, prompt construction, and LLM answer generation into a pipeline.

2. HuggingFace Embeddings (sentence-transformers/all-MiniLM-L6-v2):
   - What it does: A neural network that translates human text into dense numerical
     vectors (384 numbers per text) that capture conceptual and semantic meaning.
   - In this project: Runs completely locally on CPU/GPU without paid API keys.

3. PostgreSQL:
   - What it does: A powerful, reliable open-source relational database.
   - In this project: Acts as the primary persistent database storing chunk texts
     and their rich JSON metadata (sources, chunk IDs, timestamps).

4. pgvector Extension:
   - What it does: Extends PostgreSQL with native vector data types and vector
     similarity distance operators (e.g. cosine distance <=>).
   - In this project: Enables PostgreSQL to perform vector search directly.

5. Ollama (Local LLM runner):
   - What it does: Runs open-weights large language models (such as Llama 3)
     locally on your computer via an efficient C++ engine.
   - In this project: Generates final answers from retrieved context without
     external API calls, subscriptions, or privacy concerns.

6. Redis (In-Memory Key-Value Store):
   - What it does: An ultra-fast in-memory data store.
   - In this project: Serves as a semantic cache sitting in front of the RAG chain
     to answer identical or semantically similar queries instantly.
""")
    print("=" * 75)


def check_python_environment():
    """Checks the Python runtime and critical package imports."""
    print("\n[1/4] Checking Python Environment and Packages...")
    print(f"  * Python version: {sys.version.split()[0]}")

    required_modules = [
        ("langchain", "LangChain core"),
        ("sentence_transformers", "HuggingFace SentenceTransformers"),
        ("psycopg2", "PostgreSQL DB driver"),
        ("pgvector", "pgvector Python helper"),
        ("redis", "Redis client"),
    ]

    missing = []
    for mod_name, label in required_modules:
        try:
            __import__(mod_name)
            print(f"  [OK] {label} ('{mod_name}') is installed.")
        except ImportError:
            print(f"  [FAIL] {label} ('{mod_name}') is NOT installed.")
            missing.append(mod_name)

    if missing:
        print("\n  --> To install missing packages, run:")
        print("      pip install -r requirements.txt\n")
        return False
    return True


def check_all_services():
    """Checks all 3 local services: PostgreSQL, Redis, and Ollama."""
    all_ok = True

    # Check PostgreSQL + pgvector
    print("\n[2/4] Checking PostgreSQL + pgvector...")
    pg_ok, pg_msg = ensure_postgres_database()
    print(f"  {pg_msg}")
    if not pg_ok:
        all_ok = False

    # Check Redis
    print("\n[3/4] Checking Redis Server...")
    redis_ok, redis_msg = check_redis_connection()
    print(f"  {redis_msg}")
    if not redis_ok:
        all_ok = False

    # Check Ollama
    print(f"\n[4/4] Checking Ollama Local LLM (configured model: '{config.OLLAMA_MODEL}')...")
    ollama_ok, ollama_msg, models = check_ollama_connection()
    print(f"  {ollama_msg}")
    if not ollama_ok:
        all_ok = False

    print("\n" + "=" * 75)
    if all_ok:
        print("[SUCCESS] All environment components and local services are ready!")
    else:
        print("[ACTION REQUIRED] Some local services need your attention before running Tasks 3-6.")
        print("Review the specific '[How to fix]' instructions printed above.")
    print("=" * 75 + "\n")

    return all_ok


def main():
    print_component_explanations()
    check_python_environment()
    check_all_services()


if __name__ == "__main__":
    main()
