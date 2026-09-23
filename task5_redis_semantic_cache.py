"""TASK 5: Add Redis Semantic Cache.

Purpose:
Caching + RAG performance:
User Question -> Redis Semantic Cache -> Similar query already exists?
- Yes -> Return cached answer
- No  -> Retriever -> Relevant Chunks -> Ollama LLM -> Answer -> Store in Redis

Educational Concepts Explained:
- What caching is
- Why Redis is used
- What semantic caching means
- How a cached answer avoids repeating the RAG process
"""

import time
import json
import uuid
from typing import Dict, Any, Tuple, Optional
import numpy as np
import redis

import config
from db_utils import check_redis_connection
from task2_chunk_and_embed import get_embedding_model
from task4_retrieval_qa import query_rag_system


def print_educational_explanations():
    """Prints beginner-friendly explanations of semantic caching concepts."""
    print("=" * 75)
    print(" TASK 5: REDIS SEMANTIC CACHING FOR RAG PERFORMANCE")
    print("=" * 75)
    print("""
1. What is Caching?
   - Caching is temporarily storing the result of an expensive calculation
     (like vector search + LLM generation) in fast storage so subsequent
     identical requests can be served instantly.

2. Why is Redis used?
   - Redis is an in-memory key-value database. Since it operates directly in RAM,
     it can read and write data in under 1 millisecond, compared to seconds
     needed by a local LLM to generate tokens.

3. What does Semantic Caching mean?
   - Traditional caches require an EXACT string match:
       'What is the speed of Ingenuity?' != 'How fast does Ingenuity fly?'
     Traditional caches would fail and re-run the entire RAG pipeline.
   - Semantic Caching compares the MEANING (embeddings) of the questions:
     If the cosine similarity between the new question and a previously cached
     question exceeds our threshold (e.g. 0.88), Redis serves the cached answer!

4. How does a Cached Answer Avoid Repeating the RAG Process?
   - Cache HIT: Skips pgvector search, skips prompt building, and skips Ollama
     inference. The answer returns in ~5ms instead of 3-10 seconds!
   - Cache MISS: Executes the full RAG pipeline, returns the answer to the user,
     and saves the query, embedding, and answer into Redis for future queries.
""")
    print("=" * 75)


def get_redis_client():
    """Creates and returns a Redis client connection."""
    return redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
        decode_responses=True,
    )


def compute_cosine_similarity(vec1: list, vec2: list) -> float:
    """Computes cosine similarity between two 1D vectors."""
    a = np.array(vec1, dtype=np.float32)
    b = np.array(vec2, dtype=np.float32)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def check_semantic_cache(
    query_text: str,
    threshold: float = config.CACHE_SIMILARITY_THRESHOLD,
) -> Tuple[bool, Optional[Dict[str, Any]], float]:
    """Searches Redis for a semantically similar cached question.

    Returns:
        (hit_found, cached_entry_dict, similarity_score)
    """
    r = get_redis_client()
    cached_ids = r.smembers("semantic_cache:keys")
    if not cached_ids:
        return False, None, 0.0

    embed_model = get_embedding_model()
    query_emb = embed_model.embed_query(query_text)

    best_similarity = -1.0
    best_entry = None

    for item_id in cached_ids:
        raw_data = r.get(f"semantic_cache:item:{item_id}")
        if not raw_data:
            continue

        entry = json.loads(raw_data)
        cached_emb = entry.get("embedding", [])
        similarity = compute_cosine_similarity(query_emb, cached_emb)

        if similarity > best_similarity:
            best_similarity = similarity
            best_entry = entry

    if best_similarity >= threshold and best_entry is not None:
        return True, best_entry, best_similarity

    return False, best_entry, max(0.0, best_similarity)


def store_in_semantic_cache(query_text: str, answer: str, source_chunks: list):
    """Stores a query, its embedding vector, and its RAG answer in Redis."""
    r = get_redis_client()
    embed_model = get_embedding_model()
    query_emb = embed_model.embed_query(query_text)

    item_id = str(uuid.uuid4())[:8]
    cache_record = {
        "id": item_id,
        "query": query_text,
        "answer": answer,
        "embedding": query_emb,
        "sources_count": len(source_chunks),
        "timestamp": time.time(),
    }

    # Store entry in Redis as a JSON string
    r.set(f"semantic_cache:item:{item_id}", json.dumps(cache_record))
    # Add id to the set of cached keys
    r.sadd("semantic_cache:keys", item_id)
    print(f"[Cache Saved] Query stored in Redis (id={item_id}).")


def clear_cache():
    """Clears all semantic cache items from Redis for testing."""
    r = get_redis_client()
    cached_ids = r.smembers("semantic_cache:keys")
    for item_id in cached_ids:
        r.delete(f"semantic_cache:item:{item_id}")
    r.delete("semantic_cache:keys")
    print("[Cache Cleared] All semantic cache keys removed from Redis.")


def answer_with_semantic_cache(
    question: str,
    threshold: float = config.CACHE_SIMILARITY_THRESHOLD,
) -> Dict[str, Any]:
    """Executes the full Task 5 workflow with semantic caching."""
    # Check Redis connectivity first
    redis_ok, redis_msg = check_redis_connection()
    if not redis_ok:
        print(f"\n{redis_msg}\n")
        print("[Cache Fallback] Redis offline; falling back to direct RAG...")
        return query_rag_system(question)

    start_time = time.time()
    print(f"\n[Incoming Question] \"{question}\"")
    print(f"  -> Checking Redis semantic cache (similarity threshold = {threshold})...")

    is_hit, cached_entry, similarity = check_semantic_cache(question, threshold)
    elapsed = (time.time() - start_time) * 1000

    if is_hit:
        print(f"  [*** CACHE HIT ***] (Similarity: {similarity:.4f} >= {threshold})")
        print(f"  Matched cached question: \"{cached_entry['query']}\"")
        print(f"  Response time: {elapsed:.2f} ms (Bypassed Ollama and pgvector!)")
        return {
            "question": question,
            "answer": cached_entry["answer"],
            "cache_status": "HIT",
            "similarity": similarity,
            "matched_query": cached_entry["query"],
            "response_time_ms": elapsed,
        }

    # Cache Miss: Execute RAG
    print(f"  [--- CACHE MISS ---] (Best similarity: {similarity:.4f} < {threshold})")
    print("  -> Invoking pgvector retriever and Ollama local LLM...")

    rag_result = query_rag_system(question)
    elapsed_rag = (time.time() - start_time) * 1000

    # Store result in Redis
    store_in_semantic_cache(
        question,
        rag_result["answer"],
        rag_result.get("source_documents", []),
    )

    return {
        "question": question,
        "answer": rag_result["answer"],
        "cache_status": "MISS",
        "similarity": similarity,
        "matched_query": None,
        "response_time_ms": elapsed_rag,
    }


def main():
    print_educational_explanations()

    # Step 1: Check Redis
    redis_ok, redis_msg = check_redis_connection()
    if not redis_ok:
        print(f"\n{redis_msg}\n")
        return

    # Clear previous cache to ensure reproducible demo
    clear_cache()

    # Demo Query 1 (Fresh query -> CACHE MISS)
    q1 = "What power source does Curiosity use?"
    print("\n" + "=" * 75)
    print("RUNNING QUERY 1 (Fresh Query):")
    res1 = answer_with_semantic_cache(q1)
    print(f"Status: {res1['cache_status']} | Time: {res1['response_time_ms']:.1f}ms")
    print(f"Answer: {res1['answer']}")

    # Demo Query 2 (Semantically similar query -> CACHE HIT)
    q2 = "What is the source of electrical power for the Curiosity rover?"
    print("\n" + "=" * 75)
    print("RUNNING QUERY 2 (Near-duplicate / Semantically similar):")
    res2 = answer_with_semantic_cache(q2)
    print(f"Status: {res2['cache_status']} | Time: {res2['response_time_ms']:.1f}ms")
    print(f"Answer: {res2['answer']}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Task 5 complete: Redis semantic caching demonstrated successfully.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
