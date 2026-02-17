import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
from config import Config

class RAGEngine:
    def __init__(self):
        print("🚀 Starting RAG Engine...")
        
        # Initialize Groq (FREE and FAST!)
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            print("⚠️  WARNING: No Groq API key found!")
            print("💡 Get one free at: https://console.groq.com/")
        
        self.client = Groq(api_key=groq_api_key)
        
        # Load embeddings model
        print("📥 Loading embeddings model (this may take a minute)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Load documents
        self.vector_store = None
        self.load_documents()
        
    def load_documents(self):
        """Load documents and create vector database"""
        try:
            print("📚 Loading documents from data folder...")
            
            # Check if data folder has files
            if not os.path.exists(Config.DATA_PATH):
                print(f"⚠️  Data folder not found at {Config.DATA_PATH}")
                return
                
            files = [f for f in os.listdir(Config.DATA_PATH) if f.endswith('.txt')]
            if not files:
                print("⚠️  No .txt files found in data folder!")
                print("💡 Add some .txt files to the 'data' folder to get started!")
                return
            
            # Load all text files
            loader = DirectoryLoader(
                Config.DATA_PATH,
                glob="**/*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents = loader.load()
            
            if not documents:
                print("⚠️  No documents loaded!")
                return
            
            print(f"✅ Loaded {len(documents)} documents")
            
            # Split into chunks
            print("✂️  Splitting documents...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.CHUNK_SIZE,
                chunk_overlap=Config.CHUNK_OVERLAP
            )
            chunks = text_splitter.split_documents(documents)
            print(f"✅ Created {len(chunks)} chunks")
            
            # Create vector database
            print("💾 Building vector database...")
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            
            # Save vector store
            os.makedirs(os.path.dirname(Config.VECTOR_STORE_PATH), exist_ok=True)
            self.vector_store.save_local(Config.VECTOR_STORE_PATH)
            print("✅ Vector database ready!")
            
        except Exception as e:
            print(f"❌ Error loading documents: {e}")
    
    def ask(self, question):
        """Ask a question using RAG with Groq (FREE!)"""
        if not self.vector_store:
            return "⚠️ No documents loaded! Please add .txt files to the 'data' folder and restart the server."
        
        try:
            # Search for relevant documents
            print(f"🔍 Searching for: {question}")
            relevant_docs = self.vector_store.similarity_search(question, k=3)
            
            if not relevant_docs:
                return "I couldn't find relevant information in the database."
            
            # Build context
            context = "\n\n".join([
                f"Document {i+1}:\n{doc.page_content}" 
                for i, doc in enumerate(relevant_docs)
            ])
            
            # Create prompt
            prompt = f"""You are a helpful AI database assistant. Answer the question based on the context below.

Context from database:
{context}

Question: {question}

Instructions:
- Provide a clear, well-formatted answer
- Use bullet points for lists
- If the answer isn't in the context, say so
- Be professional and concise

Answer:"""
            
            # Get response from Groq (FREE and SUPER FAST!)
            print("🤖 Generating answer with Groq...")
            
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful database assistant that provides clear, formatted answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            print("✅ Answer generated!")
            return answer
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"Error generating answer: {str(e)}"