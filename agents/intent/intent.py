from state import Product_Info
from .prompt import INTENT_PROMPT
from config import llm
import json


class Intent_Classifier:
    
    def __init__(self, llm):
        self.llm = llm

    def intent_node(self, state: Product_Info) -> dict:

        prompt = INTENT_PROMPT.format(product=state["name"])

        response = self.llm.invoke(prompt)
        raw = response.content.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(raw)
            print("Successfully parsed data:", data)
            return {
                "intent": data["intent"],
                "intent_reason": data.get("reason", ""),
                "status": "intent_checked"
            }

        except:

            return {"intent": True, "intent_reason": "", "status": "intent_checked"}