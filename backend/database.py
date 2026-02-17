from pymongo import MongoClient
from datetime import datetime
from config import Config

class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
            self.chats = self.db["chat_history"]
            self.documents = self.db["documents"]
            print(" MongoDB connected!")
        except Exception as e:
            print(f"  MongoDB not available: {e}")
            self.client = None
        
    def save_chat(self, question, answer, metadata=None):
        """Save chat to database"""
        if not self.client:
            return None
            
        chat_entry = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        result = self.chats.insert_one(chat_entry)
        return str(result.inserted_id)
    
    def get_chat_history(self, limit=10):
        """Get recent chats"""
        if not self.client:
            return []
            
        chats = list(self.chats.find().sort("timestamp", -1).limit(limit))
        for chat in chats:
            chat["_id"] = str(chat["_id"])
            chat["timestamp"] = chat["timestamp"].isoformat()
        return chats
    
    def clear_chat_history(self):
        """Clear all chats"""
        if not self.client:
            return {"status": "MongoDB not available"}
            
        self.chats.delete_many({})
        return {"status": "Chat history cleared"}
    
    def get_stats(self):
        """Get database stats"""
        if not self.client:
            return {"chats": 0, "documents": 0}
            
        return {
            "chats": self.chats.count_documents({}),
            "documents": self.documents.count_documents({})
        }