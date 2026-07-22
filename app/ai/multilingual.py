import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

def get_translator_llm():
    """Initializes and returns the Gemini LLM for translation."""
    # Note: Requires GOOGLE_API_KEY environment variable to be set
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

def translate_english_to_kannada(text: str) -> str:
    """
    Translates English text to Kannada using Gemini.
    """
    if not text or not text.strip():
        return ""
        
    llm = get_translator_llm()
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Translate the following English text to Kannada. Provide only the translation, no other text:\n\n{text}"
    )
    chain = prompt | llm
    response = chain.invoke({"text": text})
    return response.content.strip()

def translate_kannada_to_english(text: str) -> str:
    """
    Translates Kannada text to English using Gemini.
    """
    if not text or not text.strip():
        return ""
        
    llm = get_translator_llm()
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Translate the following Kannada text to English. Provide only the translation, no other text:\n\n{text}"
    )
    chain = prompt | llm
    response = chain.invoke({"text": text})
    return response.content.strip()
