PINECONE_API_KEY_VALUE = "pcsk_7EPn1b_GYtThwVmgHy5aXghG15DKQo7dKR5syhQU2vSbdd7Ugq9cvYSfEQuBup1tZTg826"
import base64
import io
from typing import Any, List, Optional, Union
import uuid
from fastapi import File, HTTPException, UploadFile
# import pdfplumber
from utils.handle_exceptions import handle_exceptions

from src.knowledge_base.schema.knowledge_base_schema import URLPayload, FilePayload, TextPayload, KnowledgeBasePayload,ChatbotPayload

from src.knowledge_base.processing.content_collector import ContentCollector
from src.knowledge_base.processing.content_processor import ContentProcessor
from src.knowledge_base.service.vector_db_service import VectorDBService
from src.knowledge_base.processing.content_cleaning import ContentCleaning
from langchain_openai import OpenAIEmbeddings

import uuid


import os

# from agents.agent_graphh import create_agent_app

from ...agents.agent_graphh import create_agent_app

class Config:
    PINECONE_API_KEY = PINECONE_API_KEY_VALUE
    PINECONE_INDEX_NAME = "clientvenue-chatbot"
    EMBEDDING_DIMENSION = 1536 
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
    )


class KnowledgeBaseController:
    def __init__(self):
        
        self.vector_db_service = VectorDBService(Config)
        self.content_processor = ContentProcessor(chunk_size=1000, chunk_overlap=200,embedding_model="text-embedding-3-small") 
        self.content_cleaning = ContentCleaning()
       
    def _process_content(self, content: list, user: dict):
     """Process and chunk content"""
     processed_data = []
     for item in content:
         cleaned_content = self.content_cleaning.clean_html(item["content"])
         chunks = self.content_processor.chunk_content(cleaned_content)
         if chunks is not None:
             processed_data.extend({
                 "content": chunk,
                 "metadata": {**item.get("metadata", {}), "user_id": user["_id"]}
             } for chunk in chunks)
     return processed_data
     
    async def process(self, user: dict, payload: KnowledgeBasePayload):
        """Orchestrate processing of different content types"""
        try:
            content_collector = ContentCollector()
            vector_data = []
        
            # Handle different payload types
            if isinstance(payload, URLPayload):
                content = await content_collector.extract_urls(payload.urls)            
                vector_data = self._process_content(content, user)
            elif isinstance(payload, FilePayload):
                content = await content_collector.extract_files(payload.files)
                vector_data = self._process_content(content, user)
            elif isinstance(payload, TextPayload):
                content = content_collector.extract_text(payload.texts)
                vector_data = self._process_content(content, user)

            
            # Store in vector DB
            self.vector_db_service.store_chunks(vector_data, user["_id"],namespace=user["_id"])                 
            return {"status": "success", "processed_items": len(vector_data)}

        except Exception as e:
            # self.logger.error(f"Processing failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
 
    def chat_with_bot(self, user: dict, payload ):  #ChatbotPayload
        
        try:
            
            agent_app = create_agent_app(user_id= user["_id"] )
            
            result = agent_app.invoke({
                "question": payload.question,
                "history": "current_memory",
                "documents": [],
                "generation": "",
                "user_id": user["_id"]
            })
                        
            return result
            
            
            
            # vector_data = self.vector_db_service.query(payload.question, user["_id"])
            # if vector_data is not None:
                
                
            #     return {"user":user,"payload":payload,"vector": vector_data}
            # else:
            #     return {"message": "No Data"}
        except Exception as e:
            # self.logger.error(f"Processing failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        