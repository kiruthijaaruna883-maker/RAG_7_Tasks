"""TASK 4: Build the LangChain RetrievalQA RAG Chain.

Purpose:
User Question -> Retriever -> Relevant Chunks -> Ollama Local LLM -> Generated Answer

Educational Concepts Explained:
- What retrieval means
- What the retriever does
- How relevant chunks are found
- How the retrieved chunks are provided to the LLM
- How the LLM generates the final answer
- Why this is called Retrieval-Augmented Generation (RAG)
"""

from typing import List, Dict, Any, Optional
import json
import requests
from pydantic import Field

# Resilient LangChain imports for core interfaces
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document

try:
    from langchain_core.retrievers import BaseRetriever
except ImportError:
    from langchain.schema.retriever import BaseRetriever

try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain.prompts import PromptTemplate

try:
    from langchain_core.language_models.llms import LLM
except ImportError:
    from langchain.llms.base import LLM

try:
    from langchain_classic.chains import RetrievalQA
except ImportError:
    try:
        from langchain.chains import RetrievalQA
    except ImportError:
        class RetrievalQA:
            def __init__(self, llm, retriever, prompt=None):
                self.llm = llm
                self.retriever = retriever
                self.prompt = prompt

            @classmethod
            def from_chain_type(cls, llm, chain_type, retriever, return_source_documents=True, chain_type_kwargs=None):
                prompt = chain_type_kwargs.get("prompt") if chain_type_kwargs else None
                return cls(llm, retriever, prompt)

            def __call__(self, inputs: dict) -> dict:
                query = inputs["query"]
                docs = self.retriever.get_relevant_documents(query)
                context = "\n\n".join([d.page_content for d in docs])
                if self.prompt:
                    prompt_str = self.prompt.format(context=context, question=query)
                else:
                    prompt_str = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
                answer = self.llm(prompt_str)
                return {"query": query, "result": answer, "source_documents": docs}

import config
from db_utils import check_ollama_connection
from task3_store_embeddings import vector_similarity_search


def print_educational_explanations():
    """Prints beginner-friendly explanations of the RetrievalQA architecture."""
    print("=" * 75)
    print(" TASK 4: LANGCHAIN RETRIEVALQA & RAG PIPELINE")
    print("=" * 75)
    print("""
1. What does Retrieval mean?
   - Retrieval is the process of searching a knowledge base (here, PostgreSQL + pgvector)
     to locate the most relevant facts or snippets that relate to a user's question.

2. What does the Retriever do?
   - The Retriever acts as the information searcher in LangChain. It takes the user's
     natural language question, uses pgvector to find the top-K closest chunks, and
     formats them as Document objects.

3. How are Relevant Chunks Found?
   - The user's question is converted into an embedding vector using HuggingFace.
   - pgvector calculates the cosine distance between the question's vector and all
     stored chunk vectors, ordering them from smallest distance to largest.

4. How are Retrieved Chunks Provided to the LLM?
   - LangChain takes the text from the top-K chunks and pastes them into a structured
     prompt template under a '{context}' placeholder.
   - The prompt explicitly instructs the LLM: 'Answer the question based only on this context.'

5. How does the LLM Generate the Final Answer?
   - The local Ollama LLM reads both the retrieved context and the question.
   - Using its attention mechanism, it synthesizes the retrieved facts into a fluent,
     coherent natural language answer without hallucinating outside facts.

6. Why is this called Retrieval-Augmented Generation (RAG)?
   - 'Retrieval': We retrieve factual snippets from our own database.
   - 'Augmented': We augment (enrich) the LLM prompt with those factual snippets.
   - 'Generation': The LLM generates the final synthesized natural language answer.
""")
    print("=" * 75)


class PgVectorRetriever(BaseRetriever):
    """Custom LangChain Retriever connecting to PostgreSQL + pgvector."""

    top_k: int = Field(default=3)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Fetches top-k similar chunks from pgvector and wraps them in Documents."""
        results = vector_similarity_search(query, top_k=self.top_k)
        docs = []
        for r in results:
            metadata = r["metadata"] if isinstance(r["metadata"], dict) else {}
            metadata["similarity"] = r["similarity"]
            metadata["chunk_id"] = r["id"]
            docs.append(Document(page_content=r["content"], metadata=metadata))
        return docs

    def get_relevant_documents(self, query: str) -> List[Document]:
        return self._get_relevant_documents(query)


class LocalOllamaLLM(LLM):
    """Clean, direct LangChain LLM wrapper for local Ollama instance."""

    base_url: str = Field(default=config.OLLAMA_BASE_URL)
    model: str = Field(default=config.OLLAMA_MODEL)
    temperature: float = Field(default=0.0)

    @property
    def _llm_type(self) -> str:
        return "local_ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Sends the prompt to Ollama /api/generate endpoint."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        if stop:
            payload["options"]["stop"] = stop

        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                return f"[Error from Ollama: HTTP {response.status_code} - {response.text}]"
        except requests.exceptions.RequestException as e:
            return (
                f"[Error connecting to Ollama at {self.base_url}]: {e}\n"
                "Please make sure Ollama is running (`ollama serve`)."
            )


def build_retrieval_qa_chain(top_k: int = 3) -> RetrievalQA:
    """Constructs the LangChain RetrievalQA chain with custom prompt and Ollama LLM."""
    retriever = PgVectorRetriever(top_k=top_k)
    llm = LocalOllamaLLM()

    # Grounded prompt template instructing the model to rely only on context
    prompt_template = (
        "You are an assistant answering questions using retrieved reference documents.\n"
        "Strict Rule: Answer the question using ONLY the facts provided in the Context below.\n"
        "If the answer cannot be found in the Context, respond with: 'The provided documents do not contain this information.'\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    qa_prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_prompt},
    )

    return qa_chain


def query_rag_system(question: str, top_k: int = 3) -> Dict[str, Any]:
    """Runs a single question through the RAG chain and returns structured results."""
    # Check Ollama status first
    ollama_ok, ollama_msg, _ = check_ollama_connection()
    if not ollama_ok:
        print(f"\n{ollama_msg}\n")
        return {
            "question": question,
            "answer": ollama_msg,
            "source_documents": [],
        }

    qa_chain = build_retrieval_qa_chain(top_k=top_k)
    print(f"\n[RAG Query] '{question}'")
    print("  -> Searching pgvector for relevant chunks...")
    result = qa_chain({"query": question})

    answer = result.get("result", "")
    sources = result.get("source_documents", [])

    print(f"  -> Retrieved {len(sources)} relevant chunks.")
    print("  -> Generated answer via local Ollama LLM.")

    return {
        "question": question,
        "answer": answer,
        "source_documents": sources,
    }


def main():
    print_educational_explanations()

    # Test question
    sample_question = "How is the Curiosity rover powered, and what is its power output?"
    result = query_rag_system(sample_question)

    print("\n" + "=" * 75)
    print(f"QUESTION: {result['question']}")
    print("-" * 75)
    print(f"GENERATED ANSWER:\n{result['answer']}")
    print("-" * 75)
    print("RETRIEVED CHUNKS USED AS CONTEXT:")
    for idx, doc in enumerate(result["source_documents"], start=1):
        sim = doc.metadata.get("similarity", 0.0)
        print(f"\nChunk #{idx} (Similarity: {sim:.4f}):")
        print(f"Content: {doc.page_content.strip()}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
