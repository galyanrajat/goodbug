import os
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

# === FAISS DB Path ===
DB_FAISS_PATH = os.path.join("vectorstore", "db_faiss")

# === Prompt Template ===
CUSTOM_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an empathetic gut health assistant trained on trusted medical content.

Answer the question based on the context below. If the answer is not in the context, reply honestly with "Sorry, I don’t have enough information to answer that."

Context:
{context}

Question:
{question}
"""
)

# === Embedding Model ===
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === Language Model (HF endpoint) ===
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise ValueError("Please set the environment variable `HUGGINGFACEHUB_API_TOKEN`.")

    return HuggingFaceEndpoint(
        repo_id="google/flan-t5-base",
        temperature=0.5,          # now passed directly
        huggingfacehub_api_token=token
    )


# === Build Retrieval Chain ===
def build_qa_chain():
    embeddings = get_embedding_model()
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = get_llm()

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": CUSTOM_PROMPT}
    )

# === Final Function ===
def query_faiss(user_query):
    chain = build_qa_chain()
    response = chain.invoke({"query": user_query})  # Use "query" as the key
  
    return {
        "result": response["result"],
        "source_documents": response.get("source_documents", [])
    }