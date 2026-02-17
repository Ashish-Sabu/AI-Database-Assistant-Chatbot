from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RAGEngine
from database import MongoDB

# Create FastAPI app
app = FastAPI(title="AI Database Assistant")

# Enable CORS (so frontend can talk to backend)
# Configure CORS (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers
)

# Initialize components
print("\n" + "="*50)
print("AI DATABASE ASSISTANT")
print("="*50 + "\n")

rag_engine = RAGEngine()
mongo_db = MongoDB()

print("\n" + "="*50)
print("Server Ready!")
print("="*50 + "\n")

# Request/Response models
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: str

# API Endpoints
@app.get("/")
def root():
    """Check if API is running"""
    return {
        "status": "online",
        "message": "AI Database Assistant is running!",
        "version": "1.0"
    }

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    """Ask a question"""
    try:
        question = request.question.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get answer from RAG
        answer = rag_engine.ask(question)
        
        # Save to MongoDB
        mongo_db.save_chat(question, answer)
        
        return QuestionResponse(
            question=question,
            answer=answer
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(limit: int = 10):
    """Get chat history"""
    try:
        history = mongo_db.get_chat_history(limit=limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/history")
def clear_history():
    """Clear chat history"""
    try:
        result = mongo_db.clear_chat_history()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get statistics"""
    try:
        db_stats = mongo_db.get_stats()
        return {
            "total_chats": db_stats["chats"],
            "total_documents": db_stats["documents"],
            "vector_store_ready": rag_engine.vector_store is not None
        }
    except Exception as e:
        return {
            "total_chats": 0,
            "total_documents": 0,
            "vector_store_ready": False
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)