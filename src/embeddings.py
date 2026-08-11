
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle

# Default model, can be changed
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_CACHE_DIR = "data/embeddings_cache"
os.makedirs(_CACHE_DIR, exist_ok=True)

_model = None

def load_model(model_name=_MODEL_NAME):
    global _model
    if _model is None or model_name != _MODEL_NAME:
        _model = SentenceTransformer(model_name)
    return _model

def get_embeddings(texts, model_name=_MODEL_NAME):
    """Return numpy array (N,D) dtype float32 with caching"""
    if isinstance(texts, str):
        texts = [texts]
    
    cache_key = hash(tuple(texts) + (model_name,))
    cache_path = os.path.join(_CACHE_DIR, f"{cache_key}.pkl")
    
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    
    model = load_model(model_name)
    embs = model.encode(texts, show_progress_bar=False)
    embs = np.array(embs, dtype='float32')
    
    with open(cache_path, 'wb') as f:
        pickle.dump(embs, f)
    
    return embs
