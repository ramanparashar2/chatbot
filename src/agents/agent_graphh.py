

from langgraph.graph import StateGraph, START, END

from typing import Literal, List, TypedDict,Optional
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel, Field
# from openai import embeddings

# from agents.human_agent import HumanAgent
from .human_agent import HumanAgent
from config import Config
from ..tools.retrieval import RetrievalAgent
from ..tools.routing import RoutingAgent
from langchain_core.prompts import ChatPromptTemplate
from ..tools.generation import GenerationAgent


from ..tools.memory_manager import MemoryManager


class RouteQuery(BaseModel):
    datasource: Literal["vectorstore", "human"] = Field(
        ...,
        description="Select appropriate datasource based on user query",
        examples=["vectorstore", "services", "human"]  
    )

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    history: Optional[ConversationBufferMemory]
    human_transfer: bool
    user_id: str

    
system_prompt = """You are an expert at routing user questions. 
ALWAYS use one of these predefined datasources:
- vectorstore: For questions about product features, pricing plans, documentation, chathistory anser available etc
- human: When user requests human assistance or seems frustrated or prompt not able to answer

Return ONLY the datasource name, never any other text."""

def create_agent_app(user_id):
    workflow = StateGraph(GraphState)
    
    memory_manager = MemoryManager()

    
    llm, vector_store, embeddings = Config.initialize_components()
    generation_agent = GenerationAgent(llm)
    human_agent = HumanAgent()
    
    initial_history = memory_manager.load_memory(user_id)
        
    def update_memory_node(state: GraphState):
        """Node for updating conversation memory"""
        try:
            memory_manager.update_memory(
                user_id=state["user_id"],
                state={
                    "question": state["question"],
                    "generation": state["generation"]
                }
            )
            return {**state, "history": memory_manager.load_memory(state["user_id"])}
        except Exception as e:
            print(f"Memory update failed: {e}")
            return state

   

      # Setup routing
    routing_agent = RoutingAgent(
        llm=llm,
        prompt_template=ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}")
        ])
    )

    workflow.add_node("user_input", lambda state: {
        **state,
        "history": initial_history
    })
    # workflow.add_node("user_input", lambda state: state)
    workflow.add_node("update_memory", update_memory_node)

    workflow.add_node("retrieve", RetrievalAgent(user_id=user_id).execute)
    workflow.add_node("generate", generation_agent.execute)
    workflow.add_node("human", human_agent.execute)
    # workflow.add_node("update_memory", "MemoryManager().update_memory")
    
    
    workflow.add_edge(START, "user_input")
    workflow.add_conditional_edges(
        "user_input",
        lambda state: routing_agent.determine_route(state),
        {
            "vectorstore": "retrieve",
            "human": "human"
        }
    )
    
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "update_memory")
    workflow.add_edge("update_memory", END)
    # workflow.add_edge("generate",END)
    workflow.add_edge("human",END)
    
    return workflow.compile()

    



