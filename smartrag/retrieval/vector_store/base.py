from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseVectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: List[dict] = None) -> List[str]:
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        pass
