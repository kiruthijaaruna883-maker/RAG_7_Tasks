"""Central configuration for RAG Learning Project.

Provides default connection parameters and settings for:
- PostgreSQL + pgvector
- Redis Semantic Cache
- Ollama local LLM
- Local HuggingFace embedding model
- Text chunking parameters
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Base project directories
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "documents.txt"

# PostgreSQL + pgvector settings
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "rag_db")
POSTGRES_TABLE = os.getenv("POSTGRES_TABLE", "rag_documents")

# Database connection URL
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CACHE_SIMILARITY_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", 0.88))

# Ollama local LLM settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Local HuggingFace embeddings
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
)
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 384))

# Text chunking settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 350))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
