"""TASK 3: Store Embeddings with Metadata in PostgreSQL + pgvector.

Purpose:
Vector database fundamentals:
- Storing chunks, metadata, and embeddings in PostgreSQL with pgvector.
- Performing vector similarity search using the cosine distance operator (<=>).

Educational Concepts Explained:
- What pgvector is
- Why embeddings are stored in a vector database
- What metadata is
- Why metadata is stored along with the chunk
"""

import json
from typing import List, Dict, Any, Tuple
import psycopg2
from psycopg2.extras import Json
from pgvector.psycopg2 import register_vector
import numpy as np

import config
from db_utils import ensure_postgres_database
from task2_chunk_and_embed import process_documents, get_embedding_model


def print_educational_explanations():
    """Prints beginner-friendly explanations of vector database concepts."""
    print("=" * 75)
    print(" TASK 3: POSTGRESQL + PGVECTOR FUNDAMENTALS")
    print("=" * 75)
    print("""
1. What is pgvector?
   - pgvector is an open-source extension for PostgreSQL that adds native
     support for storing mathematical vectors and calculating distance between them.
   - It provides distance operators like cosine distance (<=>) and Euclidean distance (<->).

2. Why are Embeddings Stored in a Vector Database?
   - Standard relational databases compare exact text strings or numbers (e.g. WHERE name = 'Mars').
   - They cannot understand that 'satellite' and 'orbiter' have similar meanings.
   - A vector database stores the mathematical coordinates (embeddings) of text,
     allowing us to search by semantic meaning rather than exact words.

3. What is Metadata?
   - Metadata is 'data about data'. It describes the source, context, and origin
     of each chunk (e.g., source file name, chunk index, document title).

4. Why is Metadata Stored Along with the Chunk?
   - Traceability & Attribution: When the LLM answers a question, metadata lets us
     show the user exactly which document and paragraph the answer came from.
   - Filtering: It enables filtering results by category, date, or source file.
""")
    print("=" * 75)


def get_db_connection():
    """Establishes connection to PostgreSQL and registers pgvector."""
    conn = psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        dbname=config.POSTGRES_DB,
    )
    register_vector(conn)
    return conn


def create_vector_table(conn):
    """Creates the rag_documents table with vector column if it doesn't already exist."""
    with conn.cursor() as cur:
        # Create table with vector column of dimension 384
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {config.POSTGRES_TABLE} (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            metadata JSONB,
            embedding vector({config.EMBEDDING_DIMENSION})
        );
        """)
        conn.commit()
    print(f"[OK] Table '{config.POSTGRES_TABLE}' is ready in PostgreSQL.")


def store_embeddings(chunks, embeddings) -> int:
    """Stores chunks, their metadata, and their embedding vectors into PostgreSQL."""
    conn = get_db_connection()
    create_vector_table(conn)

    with conn.cursor() as cur:
        # Clear previous data for a fresh run
        cur.execute(f"TRUNCATE TABLE {config.POSTGRES_TABLE} RESTART IDENTITY;")

        insert_sql = f"""
        INSERT INTO {config.POSTGRES_TABLE} (content, metadata, embedding)
        VALUES (%s, %s, %s);
        """

        count = 0
        for chunk, emb in zip(chunks, embeddings):
            # Ensure embedding is a 1D numpy array or list
            emb_vector = np.array(emb, dtype=np.float32)
            cur.execute(
                insert_sql,
                (chunk.page_content, Json(chunk.metadata), emb_vector),
            )
            count += 1

        conn.commit()

    conn.close()
    print(f"[OK] Successfully inserted {count} records into PostgreSQL table '{config.POSTGRES_TABLE}'.")
    return count


def vector_similarity_search(query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Performs vector similarity search using pgvector cosine distance operator (<=>)."""
    embed_model = get_embedding_model()
    query_vector = np.array(embed_model.embed_query(query_text), dtype=np.float32)

    conn = get_db_connection()
    with conn.cursor() as cur:
        # pgvector cosine distance: embedding <=> query_vector
        # Cosine similarity = 1 - cosine_distance
        sql_query = f"""
        SELECT id, content, metadata, 1 - (embedding <=> %s) AS similarity
        FROM {config.POSTGRES_TABLE}
        ORDER BY embedding <=> %s
        LIMIT %s;
        """
        cur.execute(sql_query, (query_vector, query_vector, top_k))
        rows = cur.fetchall()

    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "content": row[1],
            "metadata": row[2],
            "similarity": float(row[3]),
        })

    return results


def main():
    print_educational_explanations()

    # Step 1: Verify PostgreSQL connection
    pg_ok, pg_msg = ensure_postgres_database()
    if not pg_ok:
        print(f"\n{pg_msg}\n")
        return

    # Step 2: Chunk documents and generate embeddings
    print("\n--- Generating chunks and embeddings ---")
    chunks, embeddings = process_documents()

    # Step 3: Store in PostgreSQL + pgvector
    print("\n--- Storing in PostgreSQL + pgvector ---")
    store_embeddings(chunks, embeddings)

    # Step 4: Demonstrate vector similarity search
    sample_query = "What power source does the Curiosity rover use?"
    print(f"\n--- Demonstrating Vector Similarity Search ---")
    print(f"Query: \"{sample_query}\"")
    results = vector_similarity_search(sample_query, top_k=2)

    for i, res in enumerate(results, start=1):
        print(f"\nResult #{i} (Cosine Similarity: {res['similarity']:.4f}):")
        print(f"Metadata: {res['metadata']}")
        print(f"Content:\n{res['content']}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Task 3 complete: Embeddings and metadata stored & searched in pgvector.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
