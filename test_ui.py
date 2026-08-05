import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        print("Navigating to localhost:5173...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        
        print("Clicking Knowledge Base tab...")
        await page.click("text=Knowledge Base")
        
        print("Typing question...")
        await page.fill("input[placeholder*='Ask Epidemic.Intel']", "what should be done during a cholera outbreak")
        
        print("Sending...")
        await page.click("button[type='submit']")
        
        print("Waiting for response...")
        # Wait for the bot message that contains "Cholera outbreaks can be explosive" or similar
        # Since it's demo mode, the badge should appear
        await page.wait_for_selector("text=Demo Mode (Direct Retrieval)", timeout=15000)
        
        # Give it a second to render citations and scroll to bottom
        await page.wait_for_timeout(1000)
        
        print("Taking screenshot...")
        await page.screenshot(path=r"C:\Users\Divya Tejaswi\.gemini\antigravity\brain\8a4addba-47dc-450c-b8c6-a611ce3b6a61\knowledge_panel_test.png")
        
        await browser.close()
        print("Screenshot saved to knowledge_panel_test.png")

if __name__ == "__main__":
    asyncio.run(run())
