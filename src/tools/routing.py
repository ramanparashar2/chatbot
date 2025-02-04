
from models import RouteQuery
# agents/tools/routing.py
from langchain_core.prompts import ChatPromptTemplate

class RoutingAgent:
    def __init__(self, llm, prompt_template):
        self.router = prompt_template | llm.with_structured_output(RouteQuery)
        
    def determine_route(self, state: dict) -> str: 
        print("---ROUTE QUESTION---")
        question = state["question"]
        try:
            result = self.router.invoke({"question": question})
            print(f"Routing to: {result.datasource}")
            return result.datasource
        except Exception as e:
            print(f"Routing error: {e}")
            # Fallback to vectorstore
            return "vectorstore"