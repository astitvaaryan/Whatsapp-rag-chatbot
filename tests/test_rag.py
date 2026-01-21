from app.rag.embedder import embedder
from app.utils.text_utils import clean_text, chunk_text

def test_clean_text():
    text = "  This   is  a   test.  "
    assert clean_text(text) == "This is a test."

def test_chunk_text():
    text = "word " * 100
    chunks = chunk_text(text, chunk_size=10, overlap=0)
    assert len(chunks) > 0

def test_embedder():
    # Helper to check if embedding works (requires model download)
    emb = embedder.get_embedding("Hello world")
    assert len(emb) > 0
