import os
from state import Product_Info
import json



def New_Report_Node(state: Product_Info):

    daraz_best = f"{state['daraz_results'][0]['title']} — {state['daraz_results'][0]['price']}\n            {state['daraz_results'][0]['url']}" if state.get('daraz_results') else "No Daraz listings found."
    olx_best = f"{state['olx_results'][0]['title']} — {state['olx_results'][0]['price']}" if state.get('olx_results') else "No OLX listings found."

    report = f"""RECOMMENDATION: Buy New
    
            {state['price_analysis']}

            Verdict: {state['value_verdict']}

            Best new listing from Daraz:
            {daraz_best}

            Runner-up (OLX used market):
            {olx_best}"""

    return {"final_report": report, "status": "complete"}
    


def Used_Report_Node(state: Product_Info):

    olx_best = f"{state['olx_results'][0]['title']} — {state['olx_results'][0]['price']} ({state['olx_results'][0]['location']})\n            {state['olx_results'][0]['url']}" if state.get('olx_results') else "No OLX listings found."
    daraz_best = f"{state['daraz_results'][0]['title']} — {state['daraz_results'][0]['price']}" if state.get('daraz_results') else "No Daraz listings found."

    report = f"""RECOMMENDATION: Buy Used

            {state['price_analysis']}

            Verdict: {state['value_verdict']}

            Best used listing from OLX:
            {olx_best}

            Runner-up (Daraz new):
            {daraz_best}"""

    return {"final_report": report, "status": "complete"}