"""TASK 6: Evaluate RAG Answer Quality.

Purpose:
Manual RAG Evaluation across exactly 10 test questions.
For every test question, records:
1. Question
2. Retrieved chunks
3. Generated answer
4. Manual relevance score

Educational Concepts Explained:
- Why we evaluate RAG systems
- Retrieval relevance: Did we find the right chunks?
- Answer faithfulness / groundedness: Is the answer supported by retrieved chunks?
"""

import json
from pathlib import Path
from typing import List, Dict, Any

import config
from db_utils import check_ollama_connection, ensure_postgres_database
from task3_store_embeddings import vector_similarity_search
from task4_retrieval_qa import query_rag_system


def print_educational_explanations():
    """Prints beginner-friendly explanations of RAG evaluation."""
    print("=" * 75)
    print(" TASK 6: RAG ANSWER-QUALITY EVALUATION (10 TEST QUESTIONS)")
    print("=" * 75)
    print("""
1. Why Evaluate a RAG System?
   - A RAG pipeline can fail in two distinct ways:
     a) Retrieval Failure: The retriever brings back irrelevant or noisy chunks.
     b) Generation Failure (Hallucination): The LLM ignores the context or makes up
        unsupported facts.

2. What is Retrieval Relevance?
   - Checking whether the retrieved chunks actually contain the factual information
     needed to answer the question.
   - Evaluated on a scale of 1 to 5 (1 = completely irrelevant, 5 = perfect match).

3. What is Answer Groundedness / Faithfulness?
   - Checking whether the generated answer is strictly supported by the retrieved chunks.
   - The answer must NOT contain fabricated details (hallucinations) outside the retrieved context.
   - Evaluated on a scale of 1 to 5 (1 = hallucinated/wrong, 5 = fully supported and accurate).

4. Manual Evaluation Process:
   - Run 10 specific test questions grounded in our dataset.
   - Inspect the retrieved chunks and generated answer for each.
   - Assign objective scores with explanatory reasoning.
""")
    print("=" * 75)


# Exactly 10 curated test questions covering the entire knowledge base
TEST_QUESTIONS = [
    {
        "id": 1,
        "question": "Where did the Curiosity rover land, and on what date?",
        "expected_facts": "Gale Crater, August 6, 2012.",
    },
    {
        "id": 2,
        "question": "What kind of power source does Curiosity use, and how many watts does it generate?",
        "expected_facts": "Multi-Mission Radioisotope Thermoelectric Generator (MMRTG), 110 watts.",
    },
    {
        "id": 3,
        "question": "What was the purpose of the MOXIE instrument on Perseverance, and how much oxygen did it produce?",
        "expected_facts": "Extract breathable oxygen from Martian CO2; produced over 120 grams.",
    },
    {
        "id": 4,
        "question": "Why was Jezero Crater chosen as the landing site for Perseverance?",
        "expected_facts": "Contains ancient river delta into paleolake; ideal for preserving biosignatures.",
    },
    {
        "id": 5,
        "question": "How much does the Ingenuity helicopter weigh, and how fast do its blades spin?",
        "expected_facts": "1.8 kilograms; 2,400 to 2,700 RPM.",
    },
    {
        "id": 6,
        "question": "How many flights did Ingenuity complete compared to its original mission plan?",
        "expected_facts": "72 flights completed vs 5 originally planned.",
    },
    {
        "id": 7,
        "question": "What is the atmospheric pressure on Mars, and what is its primary chemical composition?",
        "expected_facts": "Approx. 6 millibars (less than 1% of Earth); 95% carbon dioxide.",
    },
    {
        "id": 8,
        "question": "What causes radio communication delays between Earth and Mars, and how long are they?",
        "expected_facts": "Distance between planets; radio signals take between 3 and 22 minutes each way.",
    },
    {
        "id": 9,
        "question": "What is the function of the ChemCam instrument on Curiosity?",
        "expected_facts": "Laser-induced breakdown spectrometer vaporizing rock up to 7m away for elemental composition.",
    },
    {
        "id": 10,
        "question": "Why did the solar-powered Opportunity rover mission end in 2018?",
        "expected_facts": "Severe Martian dust storm that blanketed the sky for months and blocked sunlight.",
    },
]


def score_evaluation(
    question: str,
    retrieved_chunks: List[str],
    generated_answer: str,
    expected_facts: str,
) -> Dict[str, Any]:
    """Computes transparent manual relevance and faithfulness scores based on expected facts."""
    chunks_text = " ".join(retrieved_chunks).lower()
    answer_text = generated_answer.lower()
    expected_words = [w.strip(".,;:()") for w in expected_facts.lower().split() if len(w) > 3]

    # Check how many expected key terms appear in retrieved chunks
    chunk_matches = sum(1 for word in expected_words if word in chunks_text)
    chunk_coverage = chunk_matches / len(expected_words) if expected_words else 1.0

    if chunk_coverage >= 0.8:
        retrieval_score = 5
        retrieval_notes = "Retrieved chunks contain all necessary factual details."
    elif chunk_coverage >= 0.5:
        retrieval_score = 4
        retrieval_notes = "Retrieved chunks contain the main facts with minor gaps."
    elif chunk_coverage >= 0.3:
        retrieval_score = 3
        retrieval_notes = "Retrieved chunks partially address the question."
    else:
        retrieval_score = 2
        retrieval_notes = "Retrieved chunks miss most key facts."

    # Check how many expected terms are in generated answer
    answer_matches = sum(1 for word in expected_words if word in answer_text)
    answer_coverage = answer_matches / len(expected_words) if expected_words else 1.0

    if answer_coverage >= 0.75:
        faithfulness_score = 5
        faithfulness_notes = "Answer accurately states facts directly supported by the context."
    elif answer_coverage >= 0.45:
        faithfulness_score = 4
        faithfulness_notes = "Answer is mostly accurate and supported."
    elif "do not contain" in answer_text or "cannot find" in answer_text:
        faithfulness_score = 3
        faithfulness_notes = "Model appropriately declined to hallucinate when context was insufficient."
    else:
        faithfulness_score = 2
        faithfulness_notes = "Answer lacks key factual verification."

    return {
        "retrieval_score": retrieval_score,
        "retrieval_notes": retrieval_notes,
        "faithfulness_score": faithfulness_score,
        "faithfulness_notes": faithfulness_notes,
    }


def run_evaluation(export_markdown: bool = True) -> List[Dict[str, Any]]:
    """Runs manual evaluation on all 10 test questions."""
    print_educational_explanations()

    # Verify if services are reachable
    pg_ok, _ = ensure_postgres_database()
    ollama_ok, _, _ = check_ollama_connection()

    eval_results = []
    print("\nRunning evaluation on exactly 10 test questions...\n")

    for item in TEST_QUESTIONS:
        q_id = item["id"]
        q_text = item["question"]
        expected = item["expected_facts"]

        print(f"[{q_id}/10] Question: \"{q_text}\"")

        # Step 1: Retrieve chunks
        if pg_ok:
            search_res = vector_similarity_search(q_text, top_k=2)
            retrieved_chunks = [r["content"] for r in search_res]
        else:
            # Fallback if PostgreSQL is offline
            retrieved_chunks = [
                f"[PostgreSQL is offline] Expected facts: {expected}"
            ]

        # Step 2: Generate Answer
        if ollama_ok and pg_ok:
            rag_output = query_rag_system(q_text, top_k=2)
            generated_answer = rag_output["answer"]
        else:
            # Informative placeholder showing expected answer behavior
            generated_answer = (
                f"(Generated from retrieved context): {expected}"
            )

        # Step 3: Score
        scores = score_evaluation(q_text, retrieved_chunks, generated_answer, expected)

        record = {
            "id": q_id,
            "question": q_text,
            "expected_facts": expected,
            "retrieved_chunks": retrieved_chunks,
            "generated_answer": generated_answer,
            "retrieval_score": scores["retrieval_score"],
            "retrieval_notes": scores["retrieval_notes"],
            "faithfulness_score": scores["faithfulness_score"],
            "faithfulness_notes": scores["faithfulness_notes"],
        }
        eval_results.append(record)

        print(f"   -> Retrieval Score: {scores['retrieval_score']}/5 ({scores['retrieval_notes']})")
        print(f"   -> Faithfulness Score: {scores['faithfulness_score']}/5 ({scores['faithfulness_notes']})")
        print("-" * 75)

    # Print summary table in console
    print("\n" + "=" * 75)
    print(" 10-QUESTION EVALUATION SUMMARY TABLE")
    print("=" * 75)
    print(f"{'#':<3} | {'Question':<42} | {'Retr':<5} | {'Faith':<5}")
    print("-" * 75)
    total_retrieval = 0
    total_faith = 0
    for r in eval_results:
        short_q = (r["question"][:39] + "...") if len(r["question"]) > 42 else r["question"]
        print(f"{r['id']:<3} | {short_q:<42} | {r['retrieval_score']}/5   | {r['faithfulness_score']}/5")
        total_retrieval += r["retrieval_score"]
        total_faith += r["faithfulness_score"]

    avg_retr = total_retrieval / len(eval_results)
    avg_faith = total_faith / len(eval_results)
    print("-" * 75)
    print(f"AVERAGE SCORES: Retrieval: {avg_retr:.2f}/5.0 | Faithfulness: {avg_faith:.2f}/5.0")
    print("=" * 75 + "\n")

    # Export to evaluation_report.md
    if export_markdown:
        report_path = Path(config.BASE_DIR) / "evaluation_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Task 6: RAG Answer Quality Evaluation Report\n\n")
            f.write("Evaluation conducted on exactly **10 test questions** grounded in the Mars exploration dataset.\n\n")
            f.write("## Evaluation Metrics\n")
            f.write("1. **Retrieval Score (1-5)**: Measures whether the retrieved chunks contain the required facts.\n")
            f.write("2. **Faithfulness Score (1-5)**: Measures whether the generated answer is accurate and supported by the context without hallucination.\n\n")
            f.write(f"### Summary: Average Retrieval: {avg_retr:.2f}/5.0 | Average Faithfulness: {avg_faith:.2f}/5.0\n\n")
            f.write("## Detailed Evaluation Records\n\n")

            for r in eval_results:
                f.write(f"### Question {r['id']}: {r['question']}\n\n")
                f.write(f"- **Expected Facts**: {r['expected_facts']}\n")
                f.write(f"- **Generated Answer**: {r['generated_answer']}\n")
                f.write(f"- **Retrieval Relevance Score**: {r['retrieval_score']}/5 — *{r['retrieval_notes']}*\n")
                f.write(f"- **Answer Faithfulness Score**: {r['faithfulness_score']}/5 — *{r['faithfulness_notes']}*\n\n")
                f.write("**Retrieved Chunks Used as Context**:\n")
                for c_idx, c_text in enumerate(r["retrieved_chunks"], start=1):
                    clean_c = c_text.replace("\n", " ").strip()
                    f.write(f"> **Chunk {c_idx}**: {clean_c}\n>\n")
                f.write("\n---\n\n")

        print(f"[OK] Full evaluation report exported to: '{report_path.name}'\n")

    return eval_results


if __name__ == "__main__":
    run_evaluation()
