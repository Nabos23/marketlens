import os
from state import Product_Info
import json
from .prompt import MERGE_PROMPT

class Merge_Node:
    
    def __init__(self, llm):

        self.llm = llm

    def merge_node(self, state: Product_Info):

        prompt = MERGE_PROMPT.format(
            daraz_analysis = state["daraz_analysis"],
            olx_analysis = state["olx_analysis"],
            ddgs_analysis = state["ddgs_analysis"]
        )
        
        response = self.llm.invoke(prompt)
        
        raw = response.content.strip().replace("```json", "").replace("```", "")
        
        data = json.loads(raw)
        
        return {
            "price_analysis": data["price_analysis"],
            "value_verdict": data["value_verdict"],
            "price_gap_significant": data["price_gap_significant"],
            "status": "analysis_complete"
        }
