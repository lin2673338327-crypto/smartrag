from smartrag.retrieval.vector_store.chromadb import ChromaDBStore
from smartrag.document.processor import DocumentProcessor
from smartrag.llm.ollama_client import OllamaClient
from smartrag.llm.prompt import PromptTemplate

class RAGPipeline:
    def __init__(self):
        self.vector_store = ChromaDBStore()
        self.doc_processor = DocumentProcessor()
        self.llm = OllamaClient()
        self.uploaded_files = []
    
    def add_document(self, file_path: str):
        chunks = self.doc_processor.load_and_split(file_path)
        from pathlib import Path
        file_name = Path(file_path).name
        metadatas = [{"source": file_name, "chunk_id": i} for i in range(len(chunks))]
        self.vector_store.add_texts(chunks, metadatas)
        if file_name not in self.uploaded_files:
            self.uploaded_files.append(file_name)
        return len(chunks)
    
    def query(self, question: str, k: int = 3) -> str:
        results = self.vector_store.similarity_search(question, k=k)
        contexts = [doc for doc, _ in results]
        prompt = PromptTemplate.build_rag_prompt(question, contexts)
        return self.llm.generate(prompt)
    
    def get_uploaded_files(self):
        return self.uploaded_files
