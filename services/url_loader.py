from langchain_community.document_loaders import UnstructuredURLLoader
from typing import List
from langchain.schema import Document

def load_urls(urls: List[str]) -> List[Document]:
    """Load and process URLs using UnstructuredURLLoader"""
    loader = UnstructuredURLLoader(urls=urls)
    return loader.load()