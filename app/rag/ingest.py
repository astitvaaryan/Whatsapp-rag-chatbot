import os
from app.rag.embedder import embedder
from app.rag.vector_store import vector_store
from app.utils.text_utils import clean_text, chunk_text

DOCS_DIR = "data/documents"

def load_documents():
    docs = []
    if not os.path.exists(DOCS_DIR):
        print(f"Directory {DOCS_DIR} does not exist.")
        return docs

    for filename in os.listdir(DOCS_DIR):
        file_path = os.path.join(DOCS_DIR, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append({"source": filename, "content": content})
        # Add PDF support here if needed using pypdf or similar
        elif filename.endswith(".pdf"):
             print(f"PDF support not implemented yet: {filename}")
             
    return docs

def ingest_docs():
    raw_docs = load_documents()
    if not raw_docs:
        print("No documents found to ingest.")
        return

    all_chunks = []
    all_embeddings = []
    
    # Initialize index if not loaded or create new
    # For simplicity, we create a new index on every ingestion in this basic setup
    # Or determining dimension from the first embedding
    
    first_embedding = None

    for doc in raw_docs:
        cleaned_content = clean_text(doc["content"])
        chunks = chunk_text(cleaned_content)
        
        print(f"Processing {doc['source']}: {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            embedding = embedder.get_embedding(chunk)
            if first_embedding is None:
                first_embedding = embedding
                
            all_embeddings.append(embedding)
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_id": i
            })
            
    if all_embeddings:
        dimension = len(first_embedding)
        vector_store.create_index(dimension)
        vector_store.add_documents(all_embeddings, all_chunks)
        vector_store.save()
        print(f"Ingested {len(all_chunks)} chunks into vector store.")
    else:
        print("No content to ingest.")
