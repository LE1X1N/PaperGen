from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from src.config import conf
from src.errors import ChromeError


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


def capture_screenshot(driver, save_path):
    """
        Capture screenshots
    """
    try:
        time.sleep(1)
        # window size 
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)

        # save screenshot
        driver.save_screenshot(save_path)
        return save_path
    except Exception:
        raise
    

def check_driver_health():
    """
        Try to initialize a chrome driver
    """
    driver = None
    try:
        driver = init_driver()
    except ChromeError:
        raise
    finally:
        if driver is not None:
            driver.close()
            driver.quit()
