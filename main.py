# # --------------------------
# # main.py (optimized)
# # --------------------------
# from langchain import hub
# from config import Config
# from models import RouteQuery, GraphState
# from agents.tools.retrieval import RetrievalAgent
# from agents.tools.routing import RoutingAgent
# from graph_setup import WorkflowBuilder
# # from langgraph.graph import START, END, StateGraph
# from langchain.prompts import ChatPromptTemplate
# from agents.tools.generation import GenerationAgent
# from agents.tools.memory import MemoryManager
# from agents.service_agent import ServicesAgent
# # from agents.faq_agent import FAQAgent
# from agents.human_agent import HumanAgent

# system_prompt = """You are an expert at routing user questions. 
# ALWAYS use one of these predefined datasources:
# - vectorstore: For questions about product features, pricing plans, documentation
# - services: For questions about additional services or purchases
# - human: When user requests human assistance or seems frustrated

# Return ONLY the datasource name, never any other text."""

# # - faq: For policy questions, account issues, or common troubleshooting
# def create_agent_app():
#     """Factory function to create the agent workflow"""
#     # Initialize components
#     llm, vector_store = Config.initialize_components()
    
#     # Initialize agents
    
#     retriever = vector_store.as_retriever()
    
#     generation_agent = GenerationAgent(llm)
#     # faq_agent = FAQAgent(vector_store)
#     services_agent = ServicesAgent("mongodb://mandeep:d7WhvG7JDmn5Lc0N@cluster0-shard-00-00.ypstt.mongodb.net:27017,cluster0-shard-00-01.ypstt.mongodb.net:27017,cluster0-shard-00-02.ypstt.mongodb.net:27017/clientVenue?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
#     human_agent = HumanAgent()

#     # Setup routing
#     routing_agent = RoutingAgent(
#         llm=llm,
#         prompt_template=ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("human", "{question}")
#         ])
#     )

#     # Build workflow
#     workflow_builder = WorkflowBuilder()
    
#     # Add nodes
#     workflow_builder.add_node("user_input", lambda state: state)  # Passthrough node
#     workflow_builder.add_node("retrieve", RetrievalAgent(retriever).execute)
#     workflow_builder.add_node("generate", generation_agent.execute)
#     # workflow_builder.add_node("faq", faq_agent.execute)
#     workflow_builder.add_node("services", services_agent.execute)
#     workflow_builder.add_node("human", human_agent.execute)
#     workflow_builder.add_node("update_memory", MemoryManager().update_memory)
    

#     workflow_builder.add_edge(START, "user_input")
    
#     # Configure edges
#     workflow_builder.add_conditional_edge(
#         "user_input",
#         lambda state: routing_agent.determine_route(state),
#         {
#             "vectorstore": "retrieve",
#             "services": "services", 
#             "human": "human"
#         }
#     )
#             # "faq": "faq",
    
#     workflow_builder.add_edge("retrieve", "generate")
#     workflow_builder.add_edge("services", "generate")
#     workflow_builder.add_edge("generate", "update_memory")
#     # workflow_builder.add_edge("faq", "update_memory")
#     # workflow_builder.add_edge("human", "update_memory")
#     workflow_builder.add_edge("human", END)

#     workflow_builder.add_edge("update_memory", END)

#     return workflow_builder.compile()

# # Create the agent app instance
# agent_app = create_agent_app()

# def run_cli():
#     """Run the command-line interface"""
#     current_memory = MemoryManager().memory
   
#     while True:
#         try:
#             question = input("\nUser: ")
#             if question.lower() in ['exit', 'quit']:
#                 break
                
#             result = agent_app.invoke({
#                 "question": question,
#                 "history": current_memory,
#                 "documents": [],
#                 "generation": ""
#             })
            
#             current_memory = result["history"]
            
#             if result.get("human_transfer"):
#                 print("\nAssistant: Our team will contact you shortly. Please confirm your contact info:")
#             else:
#                 print(f"\nAssistant: {result['generation']}")
            
#         except KeyboardInterrupt:
#             break
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             current_memory = MemoryManager().memory


# def create_flow():
#     try:
#         with open("workflow_diagram.png", "wb") as f:
#             f.write(agent_app.get_graph().draw_mermaid_png())
#     except Exception as e:
#         print(f"Could not generate diagram: {e}")


# if __name__ == "__main__":
#     create_flow()
# #     run_cli()