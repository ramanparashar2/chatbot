from langchain.schema import Document
from typing import Dict, List

from config import Config

class RetrievalAgent:
    def __init__(self, user_id):
        self.llm, self.vector_store, self.embedding = Config.initialize_components()
        self.user_id = user_id


    def execute(self, state: Dict)-> Dict:
        print("---RETRIEVE---")
        question = state["question"]
        top_k = 2
        
        # k= top_k,filter={"user_id": user_id}
        documents = self.vector_store.similarity_search(question,k= top_k,filter={"user_id": self.user_id})
        return {"documents": documents, "question": question}
    
    