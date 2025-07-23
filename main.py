import os
import traceback
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment


from utils.scraper import Scraper
from utils.utils import read_urls_from_file
from utils.flatten_json import merge_all_json_files
from logger import Logger

from qa_interface import query_faiss  # FAISS-based retrieval
from rag_pipeline.run_rag import run_rag_pipeline  # Only for indexing

# === Paths ===
INPUT_FILE = os.path.join(r"F:\vscode main\goodbug\data\links.txt")
SCRAPE_OUTPUT_DIR = os.path.join(r"F:\vscode main\goodbug\data\raw\scraped_data")
FLATTEN_OUTPUT_DIR = os.path.join(r"F:\vscode main\goodbug\data\processed")

# === Log Files ===
LINK_LOG_FILE = os.path.join(r"F:\vscode main\goodbug\data\logs\scrape_links.log")
DATA_LOG_FILE = os.path.join(r"F:\vscode main\goodbug\data\logs\scrape_data.log")

link_logger = Logger(LINK_LOG_FILE)
data_logger = Logger(DATA_LOG_FILE)

def main():
    link_logger.info("Starting scraping + RAG pipeline.")

    # === Step 1: Scrape from URLs ===
    try:
        urls = read_urls_from_file(INPUT_FILE)
        link_logger.info(f"Read {len(urls)} URLs.")
        scraper = Scraper(SCRAPE_OUTPUT_DIR, logger=data_logger)
        scraper.scrape_links(urls)
    except Exception as e:
        link_logger.error(f"Scraping error: {e}")
        traceback.print_exc()
        return

    # === Step 2: Flatten scraped JSONs ===
    try:
        link_logger.info("Flattening scraped JSONs...")
        merge_all_json_files(SCRAPE_OUTPUT_DIR, FLATTEN_OUTPUT_DIR)
        link_logger.info("Flattened JSONs successfully.")
    except Exception as e:
        link_logger.error(f"Flattening error: {e}")
        traceback.print_exc()
        return

    # === Step 3: Run RAG pipeline (chunking + FAISS embedding) ===
    try:
        link_logger.info("Running RAG pipeline (chunking + FAISS indexing)...")
        run_rag_pipeline()
        link_logger.info("RAG pipeline completed successfully.")
    except Exception as e:
        link_logger.error(f"RAG pipeline error: {e}")
        traceback.print_exc()
        return

    # === Step 4: Query FAISS index ===
    try:
        question = "What are the signs of an unhealthy gut?"
        link_logger.info(f"Querying FAISS index: {question}")
        print("\n🔍 Running query:")
        print(question)
        result = query_faiss(question)

        print("\nAnswer:")
        print(result["result"])

        print("\nSource Documents:")
        for doc in result["source_documents"]:
            print(f"\n---\n{doc.page_content}\n(Source: {doc.metadata.get('instruction', 'N/A')})")

    except Exception as e:
        link_logger.error(f"Querying FAISS error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
