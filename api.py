# --------------------------
# api.py (updated)
# --------------------------
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import uuid
# from main import agent_app,create_flow  # Import the agent app

# from agents.tools.memory import MemoryManager
from controller.knowlege_base import extract_data

from src.knowledge_base.config.knowledge_base_route import router as knowledge_base_router


app = FastAPI(title="AI Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(knowledge_base_router)


# Session store (in-memory)
sessions: Dict[str, dict] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_route: Optional[str] = None
    

# from langchain_community.document_loaders import UnstructuredURLLoader

# @app.get("/upload")
# async def extract_from_url(request:dict):
    
#     urls = request["urls"]
#     files = request["files"]
    
#     # result = await extract_data(urls, files)
#     # return result
#     urls = [
#         "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023",
#         "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023",
#     ]
    
#     result = await extract_data(urls, files = [])
#     return result

@app.get("/")
def read_root():
    return {"message": "Backend Connected Successfully"}

@app.post("/init_session")
async def init_session():
    """Initialize a new conversation session"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        # "memory": MemoryManager(),
        "history": []
    }    
    return {"session_id": session_id}

# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest):
    
#     """Process user message through agent workflow"""
#     try:
#         # Validate session
#         if request.session_id and request.session_id not in sessions:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         # Get or create session
#         session_id = request.session_id or str(uuid.uuid4())
#         if session_id not in sessions:
#             sessions[session_id] = {
#                 "memory": MemoryManager(),
#                 "history": []
#             }
            
#         session = sessions[session_id]
               
        
        
#         # Run through agent workflow
#         result = agent_app.invoke({
#             "question": request.message,
#             "history": session["memory"].memory,
#             "documents": [],
#             "generation": ""
#         })
        
#         # Update session state
#         # session["memory"].memory = result["history"]
#         # session["history"].append({
#         #     "user": request.message,
#         #     "agent": result.get("generation", "")
#         # })
        
#         return ChatResponse(
#             response=result.get("generation", "I'm sorry, I couldn't process that"),
#             session_id=session_id,
#             agent_route=result.get("route")
#         )
        
#     except Exception as e:
#         print(e, "+++++++++++++++++++")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/history/{session_id}")
# async def get_history(session_id: str):
#     """Retrieve conversation history"""
#     if session_id not in sessions:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return sessions[session_id]["history"]

# if __name__ == "__main__":
#     # create_flow()
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)