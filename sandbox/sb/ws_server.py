import asyncio
import json
import websockets
from playwright.async_api import async_playwright

page = None
browser = None

async def launch_browser():
    global page, browser
    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=False,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://twitter.com")
    await page.wait_for_timeout(5000) # Reduced wait time for faster startup example
    print("Playwright browser launched and navigated to Twitter")
    return page # Return page for potential future use, though global is used here

async def websocket_handler(websocket, path):
    global page
    print("WebSocket client connected")
    try:
        async for message in websocket:
            if page is None:
                print("Page object not initialized yet.")
                continue
            try:
                data = json.loads(message)
                if data.get("type") == "mouse":
                    x = data.get("x")
                    y = data.get("y")
                    if x is not None and y is not None:
                        await page.mouse.move(x, y)
                        if data.get("action") == "click":
                            await page.mouse.click(x, y)
            except json.JSONDecodeError:
                print("Received invalid JSON message")
            except Exception as e:
                print(f"Error processing WebSocket message: {e}")
    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket client disconnected normally.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket client connection closed with error: {e}")
    finally:
        print("WebSocket client connection closed.")


async def main():
    global browser
    await launch_browser()
    
    host = "localhost"
    port = 3000
    
    async with websockets.serve(websocket_handler, host, port):
        print(f"WebSocket server running on ws://{host}:{port}")
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
    # try:
    #     asyncio.run(main())
    # except KeyboardInterrupt:
    #     print("Server stopped by user.")
    # finally:
    #     async def close_browser():
    #         if browser:
    #             print("Closing browser...")
    #             await browser.close()
    #             print("Browser closed.")
        
    #     if browser:
    #        try:
    #            loop = asyncio.get_event_loop()
    #            if loop.is_running():
    #                # If loop is running, create a task
    #                loop.create_task(close_browser())
    #            else:
    #                # If loop is closed or not running, run until complete
    #                asyncio.run(close_browser())
    #        except RuntimeError:
    #            # Handle cases where the loop might be closed
    #            asyncio.run(close_browser())

    #     print("Exiting application.")