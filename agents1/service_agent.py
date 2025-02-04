# agents/services_agent.py
from langchain_openai import ChatOpenAI
# from pymongo import MongoClient
from typing import Dict

from langchain.prompts import ChatPromptTemplate

class ServicesAgent:
    def __init__(self, mongo_uri):
        # self.client = MongoClient(mongo_uri)
        # self.db = self.client["service_db"]
        self.llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")
        
    def execute(self, state: Dict) -> Dict:
        print("---SERVICES AGENT WORKING---")
        # Step 1: Search services
        # services = self.db.services.aggregate([
        #     {"$search": {"text": {"query": state["question"], "path": "description"}}}
        # ])
        
        # Step 2: Generate purchase advice
        # prompt = ChatPromptTemplate.from_messages([
        #     ("system", """Analyze user query and services:
        #     Services: {services}
            
        #     1. Recommend matching services
        #     2. Add pricing info
        #     3. Provide purchase steps"""),
        #     ("human", "{question}")
        # ])
        
        # chain = prompt | self.llm
        # return {
        #     "generation": chain.invoke({
        #         "question": state["question"],
        #         "services": list(services)
        #     }).content
        # }
        return {
            "generation": "Hello"
        }