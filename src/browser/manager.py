from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

from config import SCREENSHOT_DIR
from src.utils import get_logger

logger = get_logger()

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
        command_executor="http://localhost:4444/wd/hub",
        options=chrome_options
    )

def capture_screenshot(request_id, task_id, driver):
    """
        Capture screenshots
    """
    try:
        # dir 
        save_dir = SCREENSHOT_DIR / request_id
        os.makedirs(save_dir, exist_ok=True)
        
        # window size 
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)
        
        # save screenshot
        screenshot_path = save_dir / f"task_{task_id}.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Request ID: {request_id} -> Task ID: {task_id} 截图已保存至 {screenshot_path}")
        
    except Exception as e:
        logger.info(f"Request ID: {request_id} -> Task ID: {task_id} 截屏失败 - {str(e)}")