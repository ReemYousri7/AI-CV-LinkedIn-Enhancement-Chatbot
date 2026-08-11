import os
import chromadb
from chromadb.config import Settings
from src.preprocess import load_qa_pairs
from src.embeddings import get_embeddings
import numpy as np

# Paths
DATA_CSV = "data/linkedin_career_chatbot_dataset.csv"
PERSIST_DIR = "data/chroma_db"

# Create modern client (according to new Chroma version)
client = chromadb.PersistentClient(path=PERSIST_DIR)

collection = client.get_or_create_collection(
    name="linkedin_ats",
    metadata={"hnsw:space": "cosine"}
)

# Load data from CSV if empty
if collection.count() == 0:
    print("📥 Loading dataset into Chroma...")
    qa_pairs = load_qa_pairs(DATA_CSV)
    texts = [f"{pair['question']} {pair['answer']}" for pair in qa_pairs]
    ids = [f"doc_{i}" for i in range(len(texts))]
    # Add metadata for filtering (simple categorization)
    metadatas = []
    for pair in qa_pairs:
        topic = "LinkedIn" if "linkedin" in pair['question'].lower() or "linkedin" in pair['answer'].lower() else "CV"
        metadatas.append({"topic": topic})
    embeddings = get_embeddings(texts)
    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)
    print(f"✅ Added {len(texts)} documents to Chroma.")

def retrieve_relevant_docs(query: str, top_k: int = 3):
    """Returns the closest texts from the database"""
    try:
        query_embedding = get_embeddings(query)[0]
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        docs = results["documents"][0]
        distances = results["distances"][0]
        # Re-rank by similarity (lower distance is better)
        ranked = sorted(zip(docs, distances), key=lambda x: x[1])
        docs = [doc for doc, _ in ranked[:top_k]]
        print(f"🔍 Retrieved docs for query '{query}':\n", docs)
        return docs
    except Exception as e:
        print("❌ Retrieval error:", e)
        return []
