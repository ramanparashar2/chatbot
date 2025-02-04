# --------------------------
# models.py
# --------------------------
from pydantic import BaseModel, Field
from typing import Literal, List, TypedDict,Optional
from langchain.memory import ConversationBufferMemory


class RouteQuery(BaseModel):
    datasource: Literal["vectorstore", "services", "human"] = Field(
        ...,
        description="Select appropriate datasource based on user query",
        examples=["vectorstore", "services", "human"]  
    )

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    history: Optional[ConversationBufferMemory]
    human_transfer: bool 
    # = False

