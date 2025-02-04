# agents/tools/retrieval.py
from langchain.schema import Document
from typing import Dict, List

class RetrievalAgent:
    def __init__(self, retriever):
        self.retriever = retriever

    def execute(self, state: Dict): # -> Dict:
        print("---RETRIEVE---")
        question = state["question"]
        
        
        # pc = Pinecone(api_key="pcsk_7EPn1b_GYtThwVmgHy5aXghG15DKQo7dKR5syhQU2vSbdd7Ugq9cvYSfEQuBup1tZTg826")
        # index = pc.Index(cls.PINECONE_INDEX_NAME)
        # embedding = OpenAIEmbeddings()
        # vector_store = PineconeVectorStore(embedding=embedding, index=index)
        
        # documents = self.retriever.invoke(question)
        documents = self.retriever.similarity_search(
            question,
            # top_k=2,
            # filter={"source": "tweet"},
        )
        
        print(documents, " >>>>>>>>>>>>>>>>>>>>>")
        
        # return {"documents": documents, "question": question}
    
    