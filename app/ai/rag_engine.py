import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class RAGEngine:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.3
        )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=GEMINI_API_KEY
        )

        self.vector_store = None
        self.retriever = None

    def ingest_text_files(self, data_path="backend/data"):
        loader = DirectoryLoader(
            data_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.retriever = self.vector_store.as_retriever()
        
        return self.vector_store

    def retrieve_context(self, query: str):
        if not self.retriever:
            raise ValueError("Vector store not initialized. Call ingest_text_files first.")
        
        docs = self.retriever.invoke(query)
        return docs