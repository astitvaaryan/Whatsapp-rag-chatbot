import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.ingest import ingest_docs

if __name__ == "__main__":
    ingest_docs()
