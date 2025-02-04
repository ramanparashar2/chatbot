from langchain.schema import Document
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class FAQAgent:
    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever()
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a FAQ specialist. Use ONLY these steps:
            1. Find exact matches from knowledge base
            2. Quote relevant policy numbers
            3. Keep responses under 100 words"""),
            ("human", "Question: {question}\nContext: {context}")
        ])
        self.chain = self.prompt | self.llm

    def execute(self, state: Dict) -> Dict:
        print("---FAQ AGENT WORKING---")
        docs = self.retriever.invoke(state["question"])
        context = "\n".join([d.page_content for d in docs])
        
        response = self.chain.invoke({
            "question": state["question"],
            "context": context
        })
        return {"generation": response.content, "documents": docs}