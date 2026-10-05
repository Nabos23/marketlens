import os
from state import Product_Info
import json
from .prompt import OLX_PROMPT
from agents.tools.olx_scraper import Olx_Scraper

class Olx_Agent:
    
    def __init__(self, llm):

        self.llm = llm

    def olx_node(self, state: Product_Info):

        scraper = Olx_Scraper()
        
        listings = scraper.scrape_olx(state)
        formatted = scraper.O_format_for_llm(listings)

        prompt = OLX_PROMPT.format(formatted_results=formatted)

        result = self.llm.invoke(prompt)
        analysis = result.content.strip().split('\n')
        
        return {
            "olx_results": listings,
            "olx_analysis": analysis,
            "status": "olx_complete"
        }














