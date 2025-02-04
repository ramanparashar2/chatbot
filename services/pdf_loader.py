from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain.schema import Document
import os

def load_pdf(file_path: str) -> List[Document]:
    """Load and process PDF using PyPDFLoader"""
    loader = PyPDFLoader(file_path)
    return loader.load_and_split()

def save_uploaded_file(upload_file, destination: str):
    """Utility function to save uploaded PDF"""
    with open(destination, "wb") as buffer:
        buffer.write(upload_file.file.read())