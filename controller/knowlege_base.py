

import os
from typing import List, Optional
from langchain_community.document_loaders import UnstructuredURLLoader
from unstructured.partition.auto import partition

from fastapi import File, UploadFile, Form, HTTPException
import requests

import asyncio

import tempfile





def is_pdf_url(url: str) -> bool:
    """Check if URL points to a PDF using content type detection"""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get('Content-Type', '').lower()
        return 'pdf' in content_type
    except requests.RequestException:
        return False
    
    
async def extract_data(
    
    urls: Optional[List[str]] =  Form(None), 
    files:Optional[List[UploadFile]] = File(None)
    ):
    
    extracted_content = []
    
    try:
        # Process URLs in parallel using asyncio
        if urls:
            for url in urls:
                # Use content type detection for better PDF handling
                if is_pdf_url(url):
                    elements = partition(url=url, strategy="fast")
                else:
                    elements = partition(url=url)
                
                text_content = "\n\n".join([str(el) for el in elements])
                extracted_content.append({
                    "source": url,
                    "content": text_content,
                    "type": "url"
                })

        # Process uploaded files
        if files:
            for file in files:
                # Create temporary file with proper extension
                suffix = os.path.splitext(file.filename or "")[1]
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
                    content = await file.read()
                    temp_file.write(content)
                    temp_file_path = temp_file.name

                # Process file based on extension
                elements = partition(filename=temp_file_path)
                text_content = "\n\n".join([str(el) for el in elements])
                extracted_content.append({
                    "source": file.filename,
                    "content": text_content,
                    "type": "file"
                })

                # Cleanup temporary file
                os.unlink(temp_file_path)

        return {"data": extracted_content}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))