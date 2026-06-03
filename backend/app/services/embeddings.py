from typing import List, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
except ImportError:
    EMBEDDING_MODEL = None
    

def get_embedding(text: str) -> Optional[List[float]]:
    if not EMBEDDING_MODEL:
        return None
    try:
        embedding = EMBEDDING_MODEL.encode(text, convert_to_tensor=False)
        return embedding.tolist() if isinstance(embedding, np.ndarray) else list(embedding)
    except Exception:
        return None


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    
    vec_a = np.array(vec_a)
    vec_b = np.array(vec_b)
    
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(dot_product / (norm_a * norm_b))
