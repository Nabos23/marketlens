from state import Product_Info
import json
from .prompt import DARAZ_PROMPT
from agents.tools.daraz_scraper3 import create_playwright_tools
from langgraph.prebuilt import create_react_agent

class Daraz_Agent:
    
    def __init__(self, llm):

        self.llm = llm

    def daraz_node(self, state: Product_Info):
        tools = create_playwright_tools()  # just a list now, no browser/pw to unpack
        
        try:
            agent = create_react_agent(self.llm, tools=tools)
            prompt = DARAZ_PROMPT.format(product=state.get("name"))
            
            result = agent.invoke({
                "messages": [{"role": "user", "content": prompt}]
            })

            raw = result["messages"][-1].content.strip()
            clean = raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)

            return {
                "daraz_results": data["listings"],
                "daraz_analysis": data["analysis"],
                "status": "daraz_complete"
            }
        except Exception as e:
            print(f"Daraz agent error: {e}")
            return {
                "daraz_analysis": "Failed to retrieve Daraz listings.",
                "status": "daraz_error"
            }













