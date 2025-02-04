
from fastapi import APIRouter, Depends
from src.knowledge_base.controller.knowledge_base_controller import KnowledgeBaseController
from src.knowledge_base.schema.knowledge_base_schema import KnowledgeBasePayload ,ChatbotPayload


from middleware.auth_middleware import verify_token_middleware


router = APIRouter(prefix="/knowledge_base", tags=["Knowledge Base"])



@router.post("/upload")
async def uploadKnowledgeBase(
    payload: KnowledgeBasePayload, 
    user: dict=Depends(verify_token_middleware)
    ):
    return await KnowledgeBaseController().process(user,payload)


@router.post("/chat")
def chat_with_bot (
    payload: ChatbotPayload, 
    user: dict=Depends(verify_token_middleware)
    ):
    return KnowledgeBaseController().chat_with_bot(user,payload)

    
    