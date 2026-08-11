import pytest
from src.retrieval import retrieve_relevant_docs
import chromadb
import os
import shutil

@pytest.fixture(scope="module")
def setup_test_db():
    # Use in-memory Chroma DB for testing to avoid file locks
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(name="test_linkedin_ats")

    # Add test data
    texts = ["What is LinkedIn? LinkedIn is a professional networking site.", "How to optimize CV? Use keywords."]
    ids = ["doc_0", "doc_1"]
    metadatas = [{"topic": "LinkedIn"}, {"topic": "CV"}]
    from src.embeddings import get_embeddings
    embeddings = get_embeddings(texts)
    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    yield client, collection

    # No cleanup needed for EphemeralClient

def test_retrieve_relevant_docs(setup_test_db):
    # Temporarily replace the global collection
    import src.retrieval
    original_collection = src.retrieval.collection
    client, collection = setup_test_db
    src.retrieval.collection = collection
    
    docs = retrieve_relevant_docs("What is LinkedIn?", top_k=1)
    assert len(docs) == 1
    assert "LinkedIn" in docs[0]
    
    # Test filtering
    docs_filtered = retrieve_relevant_docs("optimize", top_k=1, topic_filter="CV")
    assert len(docs_filtered) == 1
    assert "CV" in docs_filtered[0] or "optimize" in docs_filtered[0]
    
    # Restore
    src.retrieval.collection = original_collection
