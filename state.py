from typing import TypedDict, List, Dict, Annotated

def merge_status(existing: str, new: str) -> str:
    return new

class Product_Info(TypedDict):
    name: str
    product_query: List[str]
    daraz_results: List[Dict]
    olx_results: List[Dict] 
    ddgs_analysis: str
    olx_analysis: str
    daraz_analysis: str
    price_analysis: str
    value_verdict: str
    price_gap_significant: bool
    final_report: str 
    intent: bool
    intent_reason: str
    status: Annotated[str, merge_status]