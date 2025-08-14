import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RH Chatbot API"
    VERSION: str = "1.0.0"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]

    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    GROQ_MODEL: str = "llama3-8b-8192"
    EMBEDDING_MODEL: str = "thenlper/gte-large"
    
    RAG_K_THRESHOLD: int = 5
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50
    
    DATA_FILE_PATH: str = "./chat.csv"
    CONTENT_COLUMN: str = "content"
    ID_COLUMN: str = "ID"

settings = Settings()
