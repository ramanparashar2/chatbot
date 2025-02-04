import redis
import json
from typing import Dict, Any

class RedisMemoryManager:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_conversation_history(self, session_id: str) -> list:
        return self.redis.lrange(session_id, 0, -1)

    def add_to_conversation(self, session_id: str, message: Dict[str, Any]):
        self.redis.rpush(session_id, json.dumps(message))
        self.redis.expire(session_id, 3600)  # Expire after 1 hour

    def clear_conversation(self, session_id: str):
        self.redis.delete(session_id)