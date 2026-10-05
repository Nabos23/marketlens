from playwright.sync_api import sync_playwright
from langchain_core.tools import tool

def create_playwright_tools():
    """Creates browser tools that the ReAct agent can use."""

    @tool
    def navigate_and_extract(url: str) -> str:
        """Navigate to any URL and return the page text content. You may use this to search for products on other sites."""
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                return page.inner_text("body")[:12000]
            finally:
                page.close()

    @tool
    def search_and_extract(query: str) -> str:
        """Search Daraz for a product and return page text with listings."""
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()
            try:
                url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}"
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(2500)
                return page.inner_text("body")[:12000]
            finally:
                browser.close()

    return [search_and_extract, navigate_and_extract]