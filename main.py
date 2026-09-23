"""Master CLI Runner for RAG Learning Project.

Provides a clean menu to execute any of the 6 tasks individually or run
the entire end-to-end pipeline.
"""

import sys
import argparse

import task1_env_setup
import task2_chunk_and_embed
import task3_store_embeddings
import task4_retrieval_qa
import task5_redis_semantic_cache
import task6_evaluate_rag


def print_banner():
    print("""
===========================================================================
               RAG LEARNING PROJECT — 6 CORE TASKS
===========================================================================
  [1] Task 1: Environment Setup & Diagnostics
  [2] Task 2: Document Chunking & Local Embeddings
  [3] Task 3: Store in PostgreSQL + pgvector
  [4] Task 4: LangChain RetrievalQA Chain (Ollama LLM)
  [5] Task 5: Redis Semantic Cache Layer
  [6] Task 6: Evaluate RAG Quality (10 Test Questions)
  [A] Run All Tasks End-to-End
  [Q] Quit
===========================================================================
""")


def run_task(choice: str):
    choice = choice.strip().upper()
    if choice == "1":
        print("\n>>> Executing Task 1: Environment Setup & Diagnostics <<<\n")
        task1_env_setup.main()
    elif choice == "2":
        print("\n>>> Executing Task 2: Document Chunking & Embeddings <<<\n")
        task2_chunk_and_embed.process_documents()
    elif choice == "3":
        print("\n>>> Executing Task 3: Store in PostgreSQL + pgvector <<<\n")
        task3_store_embeddings.main()
    elif choice == "4":
        print("\n>>> Executing Task 4: LangChain RetrievalQA Chain <<<\n")
        task4_retrieval_qa.main()
    elif choice == "5":
        print("\n>>> Executing Task 5: Redis Semantic Cache <<<\n")
        task5_redis_semantic_cache.main()
    elif choice == "6":
        print("\n>>> Executing Task 6: Evaluate RAG Quality (10 Questions) <<<\n")
        task6_evaluate_rag.run_evaluation()
    elif choice == "A":
        print("\n>>> Executing All Tasks End-to-End <<<\n")
        task1_env_setup.main()
        task2_chunk_and_embed.process_documents()
        task3_store_embeddings.main()
        task4_retrieval_qa.main()
        task5_redis_semantic_cache.main()
        task6_evaluate_rag.run_evaluation()
    elif choice == "Q":
        print("\nExiting. Happy learning!\n")
        sys.exit(0)
    else:
        print(f"\n[Invalid selection] '{choice}'. Please select 1-6, A, or Q.\n")


def main():
    parser = argparse.ArgumentParser(description="Run RAG Learning Project Tasks")
    parser.add_argument(
        "--task",
        "-t",
        type=str,
        help="Task number to run (1-6, or 'all')",
        default=None,
    )
    args = parser.parse_args()

    if args.task:
        if args.task.lower() == "all":
            run_task("A")
        else:
            run_task(args.task)
        return

    # Interactive loop
    while True:
        print_banner()
        try:
            choice = input("Select a task to run (1-6, A, Q): ")
            run_task(choice)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
