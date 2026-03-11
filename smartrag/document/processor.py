from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from pathlib import Path
from smartrag.config import settings
import sys
import fitz
sys.modules['pymupdf'] = fitz

class DocumentProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    def load_and_split(self, file_path: str) -> List[str]:
        suffix = Path(file_path).suffix.lower()
        
        if suffix == '.pdf':
            from langchain_community.document_loaders import PyMuPDFLoader
            loader = PyMuPDFLoader(file_path)
        elif suffix in ['.txt', '.md']:
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
        
        docs = loader.load()
        chunks = self.splitter.split_documents(docs)
        return [chunk.page_content for chunk in chunks]
