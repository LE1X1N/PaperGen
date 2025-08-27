from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from src.config import conf
from src.errors import ChromeError
from src.utils import  get_logger

logger = get_logger()


def init_driver():
    """
        Init a chrome driver
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")

        return webdriver.Remote(
            command_executor=conf["selenium"]["url"],
            options=chrome_options
        )

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise ChromeError(f"Chrome Driver 初始化失败: {error_msg}") from e


def capture_screenshot(request_id, task_id, driver, save_dir):
    """
        Capture screenshots
    """
    try:
        time.sleep(1)
        # window size 
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)

        # save screenshot
        screenshot_path = save_dir / f"task_{task_id}.png"
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        logger.info(f"Request ID: {request_id} -> Task ID: {task_id} 截屏失败 - {str(e)}")
    return screenshot_path


def check_driver_health():
    driver = None
    try:
        driver = init_driver()
    except ChromeError:
        raise
    finally:
        if driver is not None:
            driver.close()
            driver.quit()
    