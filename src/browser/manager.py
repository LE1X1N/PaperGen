from playwright.sync_api import sync_playwright, Browser, Page
import base64

from src.errors import ChromeError

def open_browser_page(port: int) -> tuple[sync_playwright, Browser, Page]:
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(f"http://0.0.0.0:{port}")
        return playwright, browser, page
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise ChromeError(f"Playwright启动浏览器失败: {error_msg}") from e


def capture_screenshot(page: Page):
    """
    Capture screenshot and return as base64 string
    """
    try: 
        page.wait_for_timeout(3000)
        page.wait_for_selector("body", state="attached")    # wait for body 
        
        screenshot_bytes = page.screenshot()
        base64_str = base64.b64encode(screenshot_bytes).decode('utf-8')
        return base64_str
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise ChromeError(f"Playwright截屏失败: {error_msg}") from e
