import json
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from agents.workflow import assistant  

router = APIRouter()

@router.get("/research")
async def research(product_name: str):

    async def event_stream():
        
        initial_state = {
            "name": product_name,
            "product_query": [],
            "daraz_results": [],
            "olx_results": [],
            "ddgs_analysis": "",
            "olx_analysis": "",
            "daraz_analysis": "",
            "price_analysis": "",
            "value_verdict": "",
            "price_gap_significant": False,
            "final_report": "",
            "status": "initialized"
        }
        
        final_report = ""
        async for chunk in assistant.astream(initial_state):
            for node_name, node_output in chunk.items():
                status = node_output.get("status", node_name)
                payload = {"node": node_name, "status": status}
                yield f"data: {json.dumps(payload)}\n\n"
                
                if "final_report" in node_output:
                    final_report = node_output["final_report"]

        yield f"data: {json.dumps({'done': True, 'report': final_report})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")