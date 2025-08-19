from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from src.utils import  get_logger

logger = get_logger()

selenium_url = os.getenv("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")

def init_driver():
    """
        Init a chrome driver
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    return webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options
    )


def capture_screenshot(request_id, task_id, driver, save_dir):
    """
        Capture screenshots
    """
    try:
        # window size 
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)

        # save screenshot
        screenshot_path = save_dir / f"task_{task_id}.png"
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        logger.info(f"Request ID: {request_id} -> Task ID: {task_id} 截屏失败 - {str(e)}")

    return screenshot_path