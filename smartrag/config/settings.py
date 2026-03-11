from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    vector_store_type: str = "chromadb"
    chromadb_path: str = "./data/vector_db"
    upload_dir: str = "./data/uploads"
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    class Config:
        env_file = ".env"

settings = Settings()
