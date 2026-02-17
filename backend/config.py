import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "CHATBOT")
    
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    VECTOR_STORE_PATH = "../vector_store/faiss_index"
    DATA_PATH = "../data/"