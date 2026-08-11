import pytest
from src.preprocess import clean_text, chunk_text, load_qa_pairs
import pandas as pd
import tempfile
import os

def test_clean_text():
    text = "Hello   world! Hello  world."
    cleaned = clean_text(text)
    assert cleaned == "Hello world! Hello world."
    assert "  " not in cleaned

def test_chunk_text():
    text = "word " * 600  # 600 words
    chunks = chunk_text(text, chunk_size=500)
    assert len(chunks) == 2
    assert len(chunks[0].split()) <= 500
    assert len(chunks[1].split()) <= 500

def test_load_qa_pairs():
    # Create a temporary CSV
    data = {
        'question': ['What is LinkedIn?', 'How to write CV?'],
        'answer': ['A professional network', 'Use clear structure']
    }
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        pairs = load_qa_pairs(tmp.name)
    os.unlink(tmp.name)
    
    assert len(pairs) == 2
    assert pairs[0]['question'] == 'What is LinkedIn?'
    assert pairs[0]['answer'] == 'A professional network'
