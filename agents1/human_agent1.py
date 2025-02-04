from typing import Dict


class HumanAgent:
    def execute(self, state: Dict) -> Dict:
        print("---TRANSFERRING TO HUMAN---")
        return {
            "generation": "Our team will contact you shortly. Please confirm your contact info:",
            "human_transfer": True
        }