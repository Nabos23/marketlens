OLX_PROMPT = """You are analyzing second-hand product listings from OLX Pakistan.
These are USED products sold by individual sellers. Prices are negotiable.
Condition and authenticity cannot be guaranteed.

Product listings:
{formatted_results}

Analyze these listings and provide:
1. Price range (lowest to highest)
2. Average asking price
3. Best value listing (consider location, price, listing quality)
4. Any suspicious listings (unusually cheap, vague descriptions, etc.)
5. Overall assessment of used market availability and pricing

Be concise and factual. Note that OLX prices are typically negotiable."""