# memory_manager.py
import json
from typing import List, Dict, Union
import redis
from langchain.schema import HumanMessage, AIMessage
from pydantic import BaseModel
# from config import Config

class Config:
    REDIS_HOST="a4b2a01a8b903442d9cf4aea3c0bde77-47447699.us-east-2.elb.amazonaws.com"
    REDIS_PORT=6379
    REDIS_PASSWORD="iqS5tUJL9y2kiUlVivUd"
    REDIS_DB=0
    
    

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class MemoryManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            db=Config.REDIS_DB
        )
        self.expiration = 3600  # 1 hour expiration

    def update_memory(self, user_id: str, state: Dict) -> None:
        """Update Redis with conversation context using atomic append"""
        try:
            key = f"chat:{user_id}:history"
            
            # Create new message pair
            new_messages = [
                Message(role="user", content=state["question"]),
                Message(role="assistant", content=state["generation"])
            ]
            
            # Atomic Redis transaction
            with self.redis_client.pipeline() as pipe:
                while True:
                    try:
                        pipe.watch(key)
                        existing = pipe.get(key) or b'[]'
                        messages = json.loads(existing)
                        messages.extend([msg.dict() for msg in new_messages])
                        pipe.multi()
                        pipe.setex(key, self.expiration, json.dumps(messages))
                        pipe.execute()
                        break
                    except redis.WatchError:
                        continue
        except Exception as e:
            print(f"Redis update error: {e}")
            raise

    def load_memory(self, user_id: str) -> List[Union[HumanMessage, AIMessage]]:
        """Load conversation history as LangChain message objects"""
        try:
            key = f"chat:{user_id}:history"
            history = self.redis_client.get(key)
            if not history:
                return []
            
            messages = json.loads(history)
            langchain_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
            return langchain_messages
        except Exception as e:
            print(f"Redis load error: {e}")
            return []

    def get_raw_history(self, user_id: str) -> List[Dict]:
        """Direct access to stored messages"""
        key = f"chat:{user_id}:history"
        history = self.redis_client.get(key)
        return json.loads(history) if history else []

    @classmethod
    def from_existing(cls, user_id: str):
        """Factory method for session-aware memory"""
        instance = cls()
        # Additional session initialization if needed
        return instance