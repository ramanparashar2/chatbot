from langchain.memory import ConversationBufferMemory
from typing import Dict

class MemoryManager:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="generation"
        )

    def update_memory(self, state: Dict) -> Dict:
        """Update memory with latest interaction"""
        try:
            inputs = {"question": state["question"]}
            outputs = {"generation": state["generation"]}
            
            if state.get("human_transfer", False):
                outputs["human_transfer"] = True
            
            self.memory.save_context(inputs, outputs)
            # self.memory.save_context(
            #     {"question": state["question"]},
            #     {"generation": state["generation"]}
            # )
        except Exception as e:
            print(f"Memory update error: {e}")
        return {"history": self.memory}

    def load_memory(self) -> list:
        """Safe memory loading with fallback"""
        try:
            return self.memory.load_memory_variables({})["chat_history"]
        except KeyError:
            return []
        except Exception as e:
            print(f"Memory load error: {e}")
            return []
        
     # Keep existing methods but add session awareness
    @classmethod
    def from_existing(cls, memory_data):
        instance = cls()
        instance.memory = memory_data
        return instance