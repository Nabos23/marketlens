import os
from config import llm
from typing import Literal
from langgraph.graph import StateGraph, START, END
from state import Product_Info
from .Analysis.merge import Merge_Node
from .DARAZ.daraz_agent2 import Daraz_Agent
from .DDGS.ddgs_agent import DDGS_Agent
from .OLX.olx_agent import Olx_Agent
from .report.report_agent import Used_Report_Node, New_Report_Node
from .intent.intent import Intent_Classifier
from langgraph.types import Send

def route_verdict(state: Product_Info) -> Literal["new_report", "used_report"]:
    if state["price_gap_significant"]:
        return "used_report"
    return "new_report"

def intent_verdict(state: Product_Info):
    if not state["intent"]:
        return "reject"
    return [
        Send("daraz", state),
        Send("olx", state),
        Send("ddgs", state),
    ]

def reject_node(state: Product_Info) -> dict:
    return {
        "final_report": f"Invalid search: {state['intent_reason']}",
        "status": "rejected"
    }

workflow = StateGraph(Product_Info)

Daraz_Agent = Daraz_Agent(llm=llm)
Olx_Agent = Olx_Agent(llm=llm)
DDGS_Agent = DDGS_Agent(llm=llm)
Merge_Node = Merge_Node(llm=llm)
Intent_Classifier = Intent_Classifier(llm=llm)


workflow.add_node("intent", Intent_Classifier.intent_node)
workflow.add_node("daraz", Daraz_Agent.daraz_node)
workflow.add_node("olx", Olx_Agent.olx_node)
workflow.add_node("ddgs", DDGS_Agent.ddgs_node)
workflow.add_node("merge", Merge_Node.merge_node)
workflow.add_node("new_report", New_Report_Node)
workflow.add_node("used_report", Used_Report_Node)
workflow.add_node("reject", reject_node)


workflow.add_edge(START, "intent")

workflow.add_conditional_edges(
    "intent",
    intent_verdict,
    ["daraz", "olx", "ddgs", "reject"]  # list of possible destinations
)

workflow.add_edge("daraz", "merge")
workflow.add_edge("olx", "merge")
workflow.add_edge("ddgs", "merge")

workflow.add_conditional_edges(
    "merge",
    route_verdict,
    {
        "new_report": "new_report",
        "used_report": "used_report",
    }
)

workflow.add_edge("new_report", END)
workflow.add_edge("used_report", END)

assistant = workflow.compile()