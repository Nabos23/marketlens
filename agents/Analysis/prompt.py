MERGE_PROMPT = """You are comparing product prices across three sources in Pakistan.

Daraz (NEW):
{daraz_analysis}

OLX (USED):
{olx_analysis}

Web Search:
{ddgs_analysis}

Respond ONLY in this exact JSON format, no other text:
{{
    "price_analysis": "brief comparison of prices across all three sources",
    "value_verdict": "buy new on Daraz" or "buy used on OLX" or "check web source",
    "price_gap_significant": true or false
}}

price_gap_significant is true if OLX used price is more than 20% cheaper than Daraz new price."""