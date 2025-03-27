from playwright.async_api import async_playwright, BrowserContext
from playwright._impl._errors import TargetClosedError
import asyncio
from loguru import logger


class SandboxAgent:
    async def get_n_open_pages(self, context: BrowserContext) -> int:
        n_open = 0
        for page in context.pages:
            try:
                await page.is_visible("html")
                n_open += 1
            except TargetClosedError:
                pass
        return n_open

    async def run(self):
        async with async_playwright() as p:
            logger.info("Launching agent...")
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://playwright.dev")

            logger.info("Agent will exit once all pages have been closed ..")
            while await self.get_n_open_pages(context):
                await asyncio.sleep(1)

            await context.close()
            await browser.close()


if __name__ == "__main__":
    agent = SandboxAgent()
    asyncio.run(agent.run())