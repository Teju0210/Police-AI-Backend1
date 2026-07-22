from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.ai.rag_engine import RAGEngine

class Chatbot:
    def __init__(self, rag_engine: RAGEngine):
        self.rag_engine = rag_engine
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "context", "question"],
            template="""You are a helpful AI assistant.
Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Chat History: {chat_history}

Question: {question}
Answer:"""
        )
        self.chain = LLMChain(
            llm=self.rag_engine.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def chat(self, user_input: str) -> str:
        # Retrieve context from RAGEngine
        docs = []
        try:
            docs = self.rag_engine.retrieve_context(user_input)
        except ValueError:
            pass # Vector store might not be initialized
        
        context = "\n".join([doc.page_content for doc in docs])
        
        # Get response from LLM chain
        response = self.chain.invoke({
            "context": context,
            "question": user_input
        })
        
        return response["text"]
