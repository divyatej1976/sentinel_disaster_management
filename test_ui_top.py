import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:3000", wait_until="networkidle")
        
        await page.click("text=Knowledge Base")
        
        await page.fill("input[placeholder*='Ask Epidemic.Intel']", "what should be done during a cholera outbreak")
        await page.click("button[type='submit']")
        
        # Wait for the response to load
        await page.wait_for_selector("text=Demo Mode (Direct Retrieval)", timeout=15000)
        await page.wait_for_timeout(1000)
        
        # Scroll the messages area to the top
        await page.evaluate("document.querySelector('.overflow-y-auto').scrollTop = 0")
        await page.wait_for_timeout(500)
        
        await page.screenshot(path=r"C:\Users\Divya Tejaswi\.gemini\antigravity\brain\8a4addba-47dc-450c-b8c6-a611ce3b6a61\knowledge_panel_top.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
