DDGS_PROMPT = """You are analyzing web search results for product pricing in Pakistan.
These results may include official brand websites, tech retailers, and price comparison sites.

Search results:
{formatted_results}

Analyze these results and provide:
1. Official/MSRP price if found
2. Any retailer prices mentioned
3. Price trend (is it a new product, discontinued, etc.)
4. Availability notes (in stock, hard to find, etc.)
5. Overall assessment of market pricing from official sources

Be concise and factual. Prioritize official sources over resellers."""