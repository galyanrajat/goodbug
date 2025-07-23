import os
import json
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# === Paths ===
JSON_PATH = os.path.join("data", "processed", "merged_output.json")
DB_FAISS_PATH = os.path.join("vectorstore", "db_faiss")


def load_instruction_response_json(path):
    """Load instruction-response JSONs and convert to LangChain Documents."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = []
    for item in data:
        instruction = item.get("instruction", "").strip()
        response = item.get("response", "").strip()
        if response:
            doc = Document(
                page_content=response,
                metadata={"instruction": instruction if instruction else "N/A"}
            )
            documents.append(doc)
    print(f"Loaded {len(documents)} JSON documents.")
    return documents


def create_chunks(documents):
    """Split documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    return chunks


def get_embedding_model():
    """Load the embedding model."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def run_rag_pipeline():
    """Pipeline: Load JSON -> Chunk -> Embed -> Save FAISS."""
    print("Running RAG pipeline...")
    documents = load_instruction_response_json(JSON_PATH)
    chunks = create_chunks(documents)

    if not chunks:
        print("No chunks created. Skipping FAISS storage.")
        return

    embeddings = get_embedding_model()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"FAISS index saved at: {DB_FAISS_PATH}")


def query_faiss(question, top_k=3):
    """Query from FAISS vector DB."""
    embeddings = get_embedding_model()
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    results = db.similarity_search(question, k=top_k)
    return results


__all__ = ["run_rag_pipeline", "query_faiss"]
