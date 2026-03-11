from typing import List, Tuple
import faiss
import numpy as np
from .base import BaseVectorStore

class FAISSStore(BaseVectorStore):
    """FAISS向量库 - 内存高性能检索"""
    
    def __init__(self, dimension: int = 512):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
        self.metadatas = []
    
    def add_texts(self, texts: List[str], metadatas: List[dict] = None, embeddings: np.ndarray = None) -> List[str]:
        if embeddings is None:
            raise ValueError("FAISS需要预先计算的embeddings")
        
        self.index.add(embeddings.astype('float32'))
        self.texts.extend(texts)
        self.metadatas.extend(metadatas or [{}] * len(texts))
        return [f"doc_{i}" for i in range(len(texts))]
    
    def similarity_search(self, query_embedding: np.ndarray, k: int = 4) -> List[Tuple[str, float]]:
        distances, indices = self.index.search(query_embedding.reshape(1, -1).astype('float32'), k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.texts):
                results.append((self.texts[idx], float(1 / (1 + dist))))
        return results
