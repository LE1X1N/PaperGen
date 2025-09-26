import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.errors import ChromeError


def init_driver() -> webdriver.Remote:
    """
        Init a chrome driver
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        return webdriver.Remote(
            command_executor=f"http://{os.getenv("SELENIUM_HOST")}:{os.getenv("SELENIUM_PORT")}/wd/hub",
            options=chrome_options
        )

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise ChromeError(f"Chrome Driver 初始化失败: {error_msg}") from e


def capture_screenshot(driver : webdriver.Remote, width: int=1920, height=1080) -> str:
    """
        Capture screenshots
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)
        
        # window size 
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(width=width, height=total_height)

        # save screenshot
        base64_str = driver.get_screenshot_as_base64()
        return base64_str
    except Exception as e:
        raise ChromeError(f"Chrome Driver 截屏失败: {str(e)}") from e


def check_driver_health():
    """
        Try to initialize a chrome driver
    """
    driver = None
    try:
        driver = init_driver()
        print("Chrome Driver 检查通过！")
    except ChromeError:
        raise
    finally:
        if driver is not None:
            driver.close()
            driver.quit()
