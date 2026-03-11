from typing import List, Tuple
import chromadb
from smartrag.retrieval.vector_store.base import BaseVectorStore
from smartrag.config import settings
import uuid

class ChromaDBStore(BaseVectorStore):
    def __init__(self, collection_name: str = "smartrag"):
        self.client = chromadb.PersistentClient(path=settings.chromadb_path)
        self.collection = self.client.get_or_create_collection(collection_name)
    
    def add_texts(self, texts: List[str], metadatas: List[dict] = None) -> List[str]:
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        if metadatas is None:
            metadatas = [{"source": "uploaded", "chunk_id": i} for i in range(len(texts))]
        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)
        return ids
    
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        results = self.collection.query(query_texts=[query], n_results=k)
        return [(doc, 1 - dist) for doc, dist in zip(results['documents'][0], results['distances'][0])]
