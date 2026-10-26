
from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    print("Starting document ingestion...")

    # Check PDF folder
    if not DATA_DIR.exists():
        print(f"ERROR: Data folder not found: {DATA_DIR}")
        return

    # Load PDF documents
    print(f"Loading PDFs from: {DATA_DIR}")
    loader = PyPDFDirectoryLoader(str(DATA_DIR))
    documents = loader.load()

    if not documents:
        print("No PDF documents found. Add PDFs to the data folder.")
        return

    print(f"Loaded {len(documents)} document pages.")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    # Load local embedding model
    print("Loading local embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    # Create and populate Chroma database
    print(f"Saving documents to: {CHROMA_DIR}")

    vector_store = Chroma(
        collection_name="goalinvest_documents",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    vector_store.reset_collection()
    vector_store.add_documents(chunks)

    print("SUCCESS: Document ingestion completed!")
    print(f"Total pages: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Database location: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
