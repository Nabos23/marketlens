from playwright.sync_api import sync_playwright
from state import Product_Info
import json


class Olx_Scraper:
    
    def __init__(self):
        pass


    def scrape_olx(self, state: Product_Info, max_products: int = 5) -> list[dict]:

        query = state.get("name")
        olx_results = state.get("olx_results", [])

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()

            search_url = f"https://www.olx.com.pk/items/q-{query.replace(' ', '-')}"

            page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            cards = page.query_selector_all("article._617daaaa")

            cards = cards[:max_products]

            listings = []
            for card in cards:
                try:
                    data = card.evaluate("""el => {
                        const titleEl = el.querySelector('h2._1093b649');
                        const priceEl = el.querySelector('span.f83175ac');
                        const linkEl = el.querySelector('a[href]');
                        const locationEl = el.querySelector('span.f047db22');

                        return {
                            title: titleEl ? titleEl.innerText.trim() : 'N/A',
                            price: priceEl ? priceEl.innerText.trim() : 'N/A',
                            url: linkEl ? linkEl.getAttribute('href') : null,
                            location: locationEl ? locationEl.innerText.trim() : 'N/A',
                        }
                    }""")

                    url = data["url"]
                    if url and url.startswith("/"):
                        url = "https://www.olx.com.pk" + url

                    listings.append({
                        "title": data["title"],
                        "price": data["price"],
                        "location": data["location"],
                        "url": url,
                        "condition": "used",
                    })

                except Exception as e:
                    print(f"  Error reading card: {e}")
                    continue

            browser.close()

        return listings
            


    def O_format_for_llm(self, listings: list[dict]) -> str:

        if not listings:
            return "No listings found."

        lines = []
        for i, p in enumerate(listings, 1):
            lines.append(f"Listing {i}: {p['title']}")
            lines.append(f"  Price:     {p['price']}")
            lines.append(f"  Location:  {p['location']}")
            lines.append(f"  Condition: {p['condition']}")
            lines.append("")

        return "\n".join(lines)
