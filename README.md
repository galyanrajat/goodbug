## Gen AI Intern Task: Finetune a Gut Health Coach
Objective:
Build a conversational gut health coach that provides accurate, empathetic, and easy-to-understand answers to gut-related queries. 


# project structure

goodbug/
│
├── data/
│   ├── links.txt                          # Input file containing URLs
│   ├── logs/
│   │   ├── scrape_links.log              # Log file for link scraping
│   │   └── scrape_data.log               # Log file for data scraping
│   ├── raw/
│   │   └── scraped_data/                 # Directory for scraped JSON files
│   │       ├── link_1.json
│   │       ├── link_2.json
│   │       └── ...
│   └── processed/                        # Directory for flattened JSON files
│       └── merged_output.json
│
├── vectorstore/
│   └── db_faiss/                         # FAISS vector store
│
├── utils/
│   ├── flatten_json.py                   # Utility for flattening and merging JSON files
│   ├── scraper.py                        # Web scraping logic
│   └── utils.py                          # General utility functions
│
├── rag_pipeline/
│   ├── run_rag.py                        # RAG pipeline logic
│   └── qa_interface.py                   # Query interface for FAISS
│
├── connect_llm.py                        # New: Handles LLM connection and query logic
├── streamlit.py                         # New: Streamlit-based UI for querying the QA system
├── .env                                  # Environment variables (e.g., HF_TOKEN)
├── main.py                               # Entry point of the application
└── logger.py                             # Logging utility