from app.rag.vector_store import vector_store
from app.rag.embedder import embedder

def retrieve_context(query: str, k: int = 3):
    # Ensure store is loaded
    if vector_store.index is None:
        if not vector_store.load():
            return []
            
    query_embedding = embedder.get_embedding(query)
    results = vector_store.search(query_embedding, k)
    return results
