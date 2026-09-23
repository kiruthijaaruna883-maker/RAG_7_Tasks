"""TASK 2: Chunk Source Documents and Generate Local Embeddings.

Purpose:
Document processing pipeline:
Source Documents -> Document Loading -> LangChain TextSplitter
-> Smaller Chunks -> HuggingFace Embedding Model -> Embeddings

Educational Concepts Explained:
- What a document is
- What a chunk is
- Why documents are divided into chunks
- What an embedding is
- Why chunks are converted into embeddings
"""

from typing import List, Tuple
from pathlib import Path
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document

import config


def print_educational_explanations():
    """Prints beginner-friendly explanations of core chunking and embedding concepts."""
    print("=" * 75)
    print(" TASK 2: DOCUMENT CHUNKING & EMBEDDINGS FUNDAMENTALS")
    print("=" * 75)
    print("""
1. What is a Document?
   - A document is a raw unit of human-readable text (e.g. articles, manuals,
     reports, PDFs, or files like 'data/documents.txt') that contains knowledge.

2. What is a Chunk?
   - A chunk is a smaller, coherent excerpt or passage carved out of a larger
     document (typically 200 to 500 characters or tokens in length).

3. Why are Documents Divided into Chunks?
   - LLMs have finite context limits: Passing an entire 100-page document into
     a prompt is slow, costly, and can drown the LLM in irrelevant noise.
   - Precision: Chunking isolates specific concepts, so only the exact snippet
     relevant to the user's question is retrieved and fed to the LLM.

4. What is an Embedding?
   - An embedding is a dense array of floating-point numbers (e.g., 384 dimensions)
     produced by a neural network.
   - Words and sentences with similar meanings end up close together in this
     multi-dimensional vector space, capturing semantic relationships.

5. Why are Chunks Converted into Embeddings?
   - Traditional keyword matching (like Ctrl+F) fails when synonyms are used
     (e.g., 'power system' vs. 'battery generator').
   - By converting text to embeddings, computers can perform fast mathematical
     geometry (like cosine similarity) to find semantically relevant answers.
""")
    print("=" * 75)


def load_raw_document(file_path: Path) -> Document:
    """Loads source document text from disk into a LangChain Document object."""
    if not file_path.exists():
        raise FileNotFoundError(f"Source document not found at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc = Document(
        page_content=content,
        metadata={"source": file_path.name, "path": str(file_path)},
    )
    print(f"\n[Step 1] Loaded raw document: '{file_path.name}' ({len(content)} characters).")
    return doc


def split_document_into_chunks(
    document: Document,
    chunk_size: int = config.CHUNK_SIZE,
    chunk_overlap: int = config.CHUNK_OVERLAP,
) -> List[Document]:
    """Divides a document into smaller chunks using LangChain RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents([document])

    # Enrich metadata with chunk index
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = idx
        chunk.metadata["total_chunks"] = len(chunks)

    print(f"[Step 2] Split document into {len(chunks)} chunks "
          f"(chunk_size={chunk_size}, overlap={chunk_overlap}).")
    return chunks


def get_embedding_model():
    """Initializes the local HuggingFace embedding model without external API keys."""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
    except Exception:
        # Fallback directly to sentence-transformers
        from sentence_transformers import SentenceTransformer

        class SentenceTransformerWrapper:
            def __init__(self, model_name: str):
                self.model = SentenceTransformer(model_name)

            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                embeddings = self.model.encode(texts, show_progress_bar=False)
                return [e.tolist() for e in embeddings]

            def embed_query(self, text: str) -> List[float]:
                embedding = self.model.encode(text, show_progress_bar=False)
                return embedding.tolist()

        return SentenceTransformerWrapper(config.EMBEDDING_MODEL_NAME)


def generate_embeddings_for_chunks(
    chunks: List[Document],
) -> Tuple[List[Document], List[List[float]]]:
    """Generates 384-dimensional vector embeddings locally using HuggingFace."""
    print(f"[Step 3] Loading local HuggingFace model: '{config.EMBEDDING_MODEL_NAME}'...")
    embed_model = get_embedding_model()

    texts = [chunk.page_content for chunk in chunks]
    print(f"[Step 4] Generating embeddings for {len(texts)} chunks locally...")
    embeddings = embed_model.embed_documents(texts)
    print(f"[OK] Generated {len(embeddings)} embedding vectors.")
    return chunks, embeddings


def process_documents(file_path: Path = config.DATA_PATH):
    """Full execution of Task 2."""
    print_educational_explanations()

    # 1. Load document
    doc = load_raw_document(file_path)

    # 2. Split document into chunks
    chunks = split_document_into_chunks(doc)

    # 3. Generate embeddings
    chunks, embeddings = generate_embeddings_for_chunks(chunks)

    # Display sample chunk and its embedding representation
    sample_idx = 0
    sample_chunk = chunks[sample_idx]
    sample_emb = embeddings[sample_idx]

    print("\n" + "-" * 75)
    print(f"SAMPLE CHUNK #{sample_idx} INSPECTION:")
    print(f"Metadata: {sample_chunk.metadata}")
    print(f"Content:\n\"{sample_chunk.page_content}\"")
    print(f"Embedding vector dimension: {len(sample_emb)}")
    print(f"First 5 vector numbers: {sample_emb[:5]}")
    print("-" * 75 + "\n")

    return chunks, embeddings


if __name__ == "__main__":
    process_documents()
