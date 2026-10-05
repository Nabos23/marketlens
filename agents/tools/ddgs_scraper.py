import time
import json
from state import Product_Info
from ddgs import DDGS


class Ddgs_Scraper:
    
    def __init__(self):

        pass


    def scrape_ddgs(self, state: Product_Info, max_results: int = 5)  -> dict:

        query = state.get("name")
        product_query = state.get("product_query",[])
    
        results = []
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(
                    f"{query} price pakistan",
                    max_results=max_results,
                ))
        
            for r in search_results:
                results.append({
                    "title": r.get("title", "N/A"),
                    "snippet": r.get("body", "N/A"),
                    "url": r.get("href", "N/A"),
                    "source": "web"
                })
            
            product_query.extend(results)

        except Exception as e:
            print(f"DDGS error: {e}")

        
        return {
            "product_query":  product_query,
        }



