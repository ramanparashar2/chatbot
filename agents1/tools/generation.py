from langchain_core.prompts import ChatPromptTemplate
from typing import Dict
from langchain.memory import ConversationBufferMemory

class GenerationAgent:
    def __init__(self, llm):
        
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant. Use this context and conversation history:
            
            Context: {context}
            History: {chat_history}
            
            - Keep answers under 3 sentences
            - Be conversational
            - If unsure, say 'I don't know'"""),
            ("human", "{question}")
        ])
        
        self.chain = self.prompt | self.llm

    def execute(self, state: Dict) -> Dict:
        
        print("---GENERATING ANSWER---")        
        #multiagent start
        memory = state.get("history", ConversationBufferMemory())
    
        # Combine documents if exists
        # context = "\n\n".join([doc.page_content for doc in state.get("documents", [])])
        #multi agent end
        
        # Safe history retrieval
        try:
            chat_history = memory.load_memory_variables({}).get("chat_history", [])
        except KeyError:
            chat_history = []
        
        # Combine documents
        context = "\n\n".join([doc.page_content for doc in state["documents"]])
                
        # Generate response
        response = self.chain.invoke({
            "question": state["question"],
            "context": context,
            "chat_history": chat_history
        })
        
        return {"generation": response.content}