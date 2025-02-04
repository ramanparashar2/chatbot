import datetime
from typing import List
from typing import Optional
from fastapi import File, UploadFile
from pydantic import BaseModel, Field
from utils.objectIdPydanticAnnotation import PydanticObjectId



from pydantic import BaseModel
from typing import List, Optional, Union
from fastapi import UploadFile, File


class URLPayload(BaseModel):
    urls: List[str]
    # metadata: dict = Field(default_factory=dict)

class FilePayload(BaseModel):
    files: List[UploadFile] = File(...)
    # metadata: dict = Field(default_factory=dict)

class TextPayload(BaseModel):
    texts: List[str]
    # metadata: dict = Field(default_factory=dict)
    
class ChatbotPayload(BaseModel):
    question: str
    
KnowledgeBasePayload = Union[URLPayload, FilePayload, TextPayload]

# chatbotPayload = ChatbotPayload
