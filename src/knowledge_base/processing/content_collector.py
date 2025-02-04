# ------------------------ #
#  processing/content_collector.py  #
# ------------------------ #
import aiohttp
from fastapi import UploadFile
import pdfplumber
from io import BytesIO
from typing import List, Dict
# import docx
import logging


class ContentCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = aiohttp.ClientSession()
        
    def is_pdf_url(self, url: str) -> bool:
        return url.lower().endswith('.pdf')

    async def extract_urls(self, urls: List[str]) -> List[Dict]:
        """Extract content from web URLs"""
        results = []
        for url in urls:
            try:
                async with self.session.get(url) as response:
                    content = await response.text()
                    results.append({
                        "content": content,
                        "metadata": {"source": url, "content_type": "web"}
                    })
            except Exception as e:
                self.logger.error(f"Failed to process URL {url}: {str(e)}")
        return results

    async def extract_files(self, files: List[UploadFile]) -> List[Dict]:
        """Process uploaded files"""
        processed_files = []
        for file in files:
            try:
                content = await file.read()
                file_type = file.content_type

                if file_type == "application/pdf":
                    text = self._extract_pdf(content)
                elif file_type == "text/plain":
                    text = content.decode()
                # elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                #     text = self._extract_docx(content)
                else:
                    raise ValueError(f"Unsupported file type: {file_type}")

                processed_files.append({
                    "content": text,
                    "metadata": {
                        "filename": file.filename,
                        "content_type": file_type
                    }
                })
            except Exception as e:
                self.logger.error(f"Failed to process file {file.filename}: {str(e)}")
            finally:
                await file.close()
        return processed_files

    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from PDF files"""
        text = []
        with pdfplumber.open(BytesIO(content)) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text())
        return "\n".join(text)

    # def _extract_docx(self, content: bytes) -> str:
    #     """Extract text from Word documents"""
    #     doc = docx.Document(BytesIO(content))
    #     return "\n".join([para.text for para in doc.paragraphs])

    def extract_text(self, texts: List[str]) -> List[Dict]:
        """Process direct text input"""
        return [{"content": text, "metadata": {"content_type": "raw_text"}} 
                for text in texts]