
import os
from langchain import hub
from pinecone import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import langchain.vectorstores.pinecone as pinecone
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from typing import Literal, List, TypedDict


from dotenv import load_dotenv
load_dotenv(override=True)

prompt = hub.pull("hwchase17/openai-tools-agent")

llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")


pc = Pinecone()

index_name = "pdf"
index = pc.Index(index_name)

embedding = OpenAIEmbeddings()

vector_store = PineconeVectorStore(embedding=embedding, index=index)

query = "starter plan pricing"


results = vector_store.similarity_search(query, k=1)

retriever = vector_store.as_retriever()






class RouteQuery(BaseModel): 
    
    datasource: Literal["vectorstore"]= Field(
        ...,
        description="The datasource to use for the query",
    )
    

structured_llm_router = llm.with_structured_output(RouteQuery)


# Prompt
system = """You are an expert at routing a user question to a vectorstore.
Use the vectorstore for questions on these topics. """
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router
# print(
#     question_router.invoke(
#         {"question": "starter plan pricing?"}
#     )
# )
# print(question_router.invoke({"question": "starter plan pricing?"}))




class GraphState(TypedDict):
    question:str
    generation:str
    documents: List[str]
    

from langchain.schema import Document


def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}




def route_question(state):
    """
    Route question to wiki search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    question = state["question"]
    source = question_router.invoke({"question": question})
    # if source.datasource == "wiki_search":
    #     print("---ROUTE QUESTION TO Wiki SEARCH---")
    #     return "wiki_search"
    # elif 
    # source.datasource == "vectorstore":
    print("---ROUTE QUESTION TO RAG---", source)
    return "vectorstore"

from langgraph.graph import END, StateGraph, START

workflow = StateGraph(GraphState)
# Define the nodes
# workflow.add_node("wiki_search", wiki_search)  # web search
workflow.add_node("retrieve", retrieve)  # retrieve

# Build graph
workflow.add_conditional_edges(
    START,
    route_question,
    {
        # "wiki_search": "wiki_search",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge( "retrieve", END)
# workflow.add_edge( "wiki_search", END)
# Compile
app = workflow.compile()


from langchain.tools import BaseTool



from IPython.display import Image, display

try:
    # display(Image(app.get_graph().draw_mermaid_png()))
    with open("output_image.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
except Exception:
    # This requires some extra dependencies and is optional
    pass


