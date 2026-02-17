# 🤖 AI Database Assistant Chatbot

A powerful AI chatbot that answers questions from your company database using RAG (Retrieval Augmented Generation).

## 🚀 Features

- 🧠 RAG (Retrieval Augmented Generation)
- 💾 MongoDB for chat history
- 🔍 FAISS Vector Database
- ⚡ Groq AI (Free & Fast)
- 🎨 Beautiful Web Interface
- 📄 Upload custom documents

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI
- **AI:** Groq (LLaMA 3.3 70B)
- **Vector DB:** FAISS
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript
- **Embeddings:** HuggingFace (all-MiniLM-L6-v2)

## 📋 Requirements

- Python 3.12+
- MongoDB (local or Atlas)
- Groq API Key (FREE)

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Database-Assistant-Chatbot.git
cd AI-Database-Assistant-Chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```bash
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=CHATBOT
```

### 5. Add your data
- Add `.txt` files to the `data/` folder

### 6. Run the backend
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0
```

### 7. Run the frontend
```bash
cd frontend
python -m http.server 3000
```

### 8. Open browser
```
http://localhost:3000
```

## 🔑 Get Free Groq API Key

1. Go to: https://console.groq.com/
2. Sign up (free)
3. Create API key
4. Add to `.env` file

## 📁 Project Structure
```
CHATBOT/
├── backend/
│   ├── app.py              # FastAPI server
│   ├── rag_engine.py       # RAG logic
│   ├── database.py         # MongoDB connection
│   └── config.py           # Configuration
├── frontend/
│   └── index.html          # Web interface
├── data/                   # Add your .txt files here
├── .env                    # API keys (not uploaded)
├── .gitignore
├── README.md
└── requirements.txt
```

## 📸 Screenshots

[Add screenshots of your chatbot here]

## 🤝 Contributing

Pull requests are welcome!

## 📝 License

MIT License