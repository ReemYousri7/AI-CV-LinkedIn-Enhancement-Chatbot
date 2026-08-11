import re
import pandas as pd

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0600-\u06FF0-9A-Za-z .,?!\n\r-]', '', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks

def load_qa_pairs(csv_path: str) -> list:
    df = pd.read_csv(csv_path)
    qa_pairs = []
    for _, row in df.iterrows():
        qa_pairs.append({
            'question': row['question'],
            'answer': row['answer']
        })
    return qa_pairs


