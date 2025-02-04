from langchain_core.prompts import ChatPromptTemplate
from typing import Dict
from langchain.memory import ConversationBufferMemory

from ..tools.memory_manager import MemoryManager

from langchain.schema import HumanMessage, AIMessage



class GenerationAgent:
    def __init__(self, llm):
        
        self.llm = llm
        self.memory_manager = MemoryManager()
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
    
    def _format_history(self, messages: list) -> str:
        """Convert message objects to formatted conversation string"""
        formatted = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted.append(f"Human: {msg.content}")
            elif isinstance(msg, AIMessage):
                formatted.append(f"Assistant: {msg.content}")
        return "\n".join(formatted[-6:])

    def execute(self, state: Dict) -> Dict:
        print("---GENERATING ANSWER---")        
        
        user_id = state.get("user_id", "")
        if not user_id:
                raise ValueError("Missing user_id in state")
            
         # Retrieve and format history
        raw_history = self.memory_manager.load_memory(user_id)
        chat_history = self._format_history(raw_history)
        
        context = "\n\n".join([doc.page_content for doc in state["documents"]])
                        
        # Generate response
        response = self.chain.invoke({
            "question": state["question"],
            "context": context,
            "chat_history": chat_history
        })
        
        print(response, " ZZZZZZZZZZZZZZZZZZZZZZzzzzzzzzzzzzzzzzzzzzzzz")
        
        return {"generation": response.content}