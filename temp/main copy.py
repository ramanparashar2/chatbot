# --------------------------
# main.py
# --------------------------
from langchain import hub
from config import Config
from models import RouteQuery, GraphState
from agents.tools.retrieval import RetrievalAgent
from agents.tools.routing import RoutingAgent
from graph_setup import WorkflowBuilder
from langgraph.graph import START, END, StateGraph
from langchain.prompts import ChatPromptTemplate
from agents.tools.generation import GenerationAgent
from agents.tools.memory import MemoryManager

from agents.service_agent import ServicesAgent
from agents.faq_agent import FAQAgent
from agents.human_agent import HumanAgent

# system_prompt  ="""You are an expert at routing user questions. 
# ALWAYS use one of these predefined datasources:
# - vectorstore: For questions about product features, pricing plans, documentation, or technical details

# Return ONLY the datasource name, never any other text."""

system_prompt = """You are an expert at routing user questions. 
ALWAYS use one of these predefined datasources:
- vectorstore: For questions about product features, pricing plans, documentation
- faq: For policy questions, account issues, or common troubleshooting
- services: For questions about additional services or purchases
- human: When user requests human assistance or seems frustrated

Return ONLY the datasource name, never any other text."""

def main():
    # Initialize components
    llm, vector_store = Config.initialize_components()
    
    
    retriever = vector_store.as_retriever()
    generation_agent = GenerationAgent(llm)
    
    
    #multi agent start
    faq_agent = FAQAgent(vector_store)
    services_agent = ServicesAgent("mongodb://localhost:27017")
    human_agent = HumanAgent()
    
    #multiagent end
    
    # Initialize memory
    memory_manager = MemoryManager()



    # Setup agents
    retrieval_agent = RetrievalAgent(retriever)
    routing_agent = RoutingAgent(
        llm=llm,
        prompt_template=ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}")
        ])
    )

    # Build workflow
    workflow_builder = WorkflowBuilder()
    # workflow_builder.add_node("retrieve", retrieval_agent.execute)
    # workflow_builder.add_node("generate", generation_agent.execute)  # Add this line
    # workflow_builder.add_node("update_memory", memory_manager.update_memory)
    
    # Add multiagent nodes
    workflow_builder.add_node("retrieve", RetrievalAgent(retriever).execute)
    workflow_builder.add_node("generate", generation_agent.execute)
    workflow_builder.add_node("faq", faq_agent.execute)
    workflow_builder.add_node("services", services_agent.execute)
    workflow_builder.add_node("human", human_agent.execute)
    workflow_builder.add_node("update_memory", memory_manager.update_memory)
    # add multi agent end

    workflow_builder.add_conditional_edge(
        START,
        lambda state: routing_agent.determine_route(state),
        {
            # "vectorstore": "retrieve"
            "vectorstore": "retrieve",
            "faq": "faq",
            "services": "services", 
            "human": "human"
        }
    )
    
    # Update edges
    workflow_builder.add_edge("retrieve", "generate")
    workflow_builder.add_edge("generate", "update_memory")  
    
    # multiagent start
    # Connect direct paths
    workflow_builder.add_edge("faq", "update_memory")
    workflow_builder.add_edge("services", "update_memory")
    workflow_builder.add_edge("human", "update_memory")
    #multi agent end
    workflow_builder.add_edge("update_memory", END)
    app = workflow_builder.compile()
    
    
    # initial_state = {
    #     "question": "",
    #     "documents": [],
    #     "generation": "",
    #     "history": memory_manager.memory
    # }

    # Example usage
    # state = {"question": "starter plan pricing?"}
    # result = app.invoke(state)
    # print(result["generation"])

    # Save workflow visualization
    try:
        with open("workflow_diagram.png", "wb") as f:
            f.write(app.get_graph().draw_mermaid_png())
    except Exception as e:
        print(f"Could not generate diagram: {e}")
        
    # try:
    #     test_state = {
    #         **initial_state,
    #         "question": "starter plan pricing?"
    #     }
    #     result = app.invoke(test_state)
    #     print("Final Answer:", result["generation"])
    # except Exception as e:
    #     print(f"Execution error: {e}")
    
    
    
    
    # Conversation loop
    current_memory = MemoryManager().memory
    while True:
        try:
            question = input("\nUser: ")
            if question.lower() in ['exit', 'quit']:
                break
                
            result = app.invoke({
                "question": question,
                "history": current_memory,
                "documents": [],
                "generation": ""
            })
            
            current_memory = result["history"]
            
            # Handle human transfer
            if result.get("human_transfer"):
                print("\nAssistant: Our team will contact you shortly. Please confirm your contact info:")
            else:
                print(f"\nAssistant: {result['generation']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            current_memory = MemoryManager().memory
            
    return app

if __name__ == "__main__":
    # main()
    app = main()

    
     # Conversation loop
    current_memory = MemoryManager().memory  # Start fresh session
    while True:
        try:
            question = input("\nUser: ")
            if question.lower() in ['exit', 'quit']:
                break
                
            result = app.invoke({
                "question": question,
                "history": current_memory,
                "documents": [],
                "generation": ""
            })
            
            current_memory = result["history"]
            print(f"\nAssistant: {result['generation']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            current_memory = MemoryManager().memory