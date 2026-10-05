from state import Product_Info
import json
from .prompt import DDGS_PROMPT
from agents.tools.ddgs_scraper import Ddgs_Scraper

class DDGS_Agent:
    
    def __init__(self, llm):

        self.llm = llm

    def ddgs_node(self, state: Product_Info):

        scraper = Ddgs_Scraper()
        
        scraper.scrape_ddgs(state)

        product_query = state.get("product_query",[])

        prompt = DDGS_PROMPT.format(formatted_results=product_query)

        result = self.llm.invoke(prompt)
        analysis = result.content.strip()
        
        return {
            "ddgs_analysis": analysis,
            "status": "ddgs_complete"
        }