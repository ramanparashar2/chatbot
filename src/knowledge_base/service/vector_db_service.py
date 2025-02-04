

# from chromadb.config import Settings as ChromaSettings

from openai import embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from typing import List, Dict
import uuid
import asyncio

from langchain_core.documents import Document


class VectorDBService:
    def __init__(self, config):
        
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        index = pc.Index(config.PINECONE_INDEX_NAME)
        self.vector_store = PineconeVectorStore(index=index, embedding=config.embeddings)
        
        # PineconeVectorStore.from_existing_index(
        #     index_name= config.PINECONE_INDEX_NAME,
        #     embedding=config.embeddings
        # )

    def store_chunks(self, chunks: List[Dict], user_id: str,namespace:str):
        """Store chunks in user-specific namespace"""
        try:
            texts = [chunk["content"] for chunk in chunks]
            metadatas = [{
                **chunk["metadata"],
                "user_id": user_id
            } for chunk in chunks]
            
            # ids = [str(idx) for idx in range(len(chunks))]
            ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
            
            documents = [Document(page_content=chunk['content'], metadata=chunk['metadata']) for chunk in chunks]
            self.vector_store.add_documents(documents=documents,ids=ids)
            
            # await asyncio.to_thread(
            #     self.vector_store.add_texts,
            #     texts=texts,
            #     metadatas=metadatas,
            #     ids=ids,
            #     namespace=user_id 
            # )
            
        except Exception as e:
            print(f"Storage failed: {str(e)}")
            raise

    def query(self, query_embedding: str , user_id: str, top_k:int =2):  #List[float]
        """Query within user-specific namespace"""
        try:
            return self.vector_store.similarity_search( query_embedding, k= top_k,filter={"user_id": user_id})
            
            # cos =  await asyncio.to_thread(
            #     self.vector_store.similarity_search_by_vector,
            #     embedding=query_embedding,
            #     k=top_k,
            #     namespace=user_id,
            #     filter={"user_id": user_id}  # Additional security filter
            # )
            # print(cos, " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # return "cos"
        except Exception as e:
            # self.logger.error(f"Query failed: {str(e)}")
            print(f"Storage failed: --------------------- {str(e)}")
            raise