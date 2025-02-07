
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv(override=True)


import logging
import os
openai_api_key = os.getenv("OPENAI_API_KEY")


class ContentProcessor:
    def __init__(self, chunk_size: int, chunk_overlap: int, embedding_model: str):
        self.logger = logging.getLogger(__name__)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        self.embedding_model = OpenAIEmbeddings(model=embedding_model)


    def chunk_content(self, text: str):
        """Split text into semantic chunks"""
        try:
            return self.text_splitter.split_text(text)
        except Exception as e:
            self.logger.error(f"Chunking failed: {str(e)}")
            return [text]

    def generate_embeddings(self, chunks: List[str]) ->List[List[float]]:
        """Generate vector embeddings for text chunks"""
        try:
            return self.embedding_model.embed_documents(chunks)
        except Exception as e:
            self.logger.error(f"Embedding generation failed: {str(e)}")
            raise