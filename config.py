import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv(override=True)


class Config:
    PINECONE_INDEX_NAME = "clientvenue-chatbot"
    LLM_MODEL = "gpt-3.5-turbo"
    EMBEDDING_LLM_MODEL="text-embedding-3-small"
    LLM_TEMPERATURE = 0.6

    @classmethod
    def initialize_components(cls):
        pc = Pinecone(api_key="pcsk_7EPn1b_GYtThwVmgHy5aXghG15DKQo7dKR5syhQU2vSbdd7Ugq9cvYSfEQuBup1tZTg826")
        index = pc.Index(cls.PINECONE_INDEX_NAME)
        embedding = OpenAIEmbeddings(model=Config.EMBEDDING_LLM_MODEL)
        vector_store = PineconeVectorStore(embedding=embedding, index=index)        
        llm = ChatOpenAI(temperature=cls.LLM_TEMPERATURE, model=cls.LLM_MODEL)
        return llm, vector_store, embedding