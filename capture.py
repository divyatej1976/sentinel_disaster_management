import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 1024})
        await page.goto("http://localhost:3000")
        await page.click("text='Run Consensus Simulation'")
        # Wait for the loading state to appear and then disappear
        await page.wait_for_timeout(500)
        await page.wait_for_selector("text='Synthesizing Consensus...'", state="hidden", timeout=25000)
        # Give Framer Motion animations time to settle
        await page.wait_for_timeout(1500)
        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()

asyncio.run(run())
