import time
import logging
import subprocess
import os
from typing import Optional

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

load_dotenv()


class Program:
    def __init__(self, existing_session=False):
        self.existing_session = existing_session
        self.options = Options()
        self.service: Optional[Service] = None
        self.driver: webdriver.Chrome
        self.chrome_exec_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self._setup_webdriver()

    def _setup_webdriver(self) -> None:
        try:
            from webdriver_manager.chrome import ChromeDriverManager

            self.service = Service(ChromeDriverManager().install())
        except ImportError:
            logging.warning("Import error with ChromeDriverManager")
            self.service = None
        if self.existing_session:
            self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        else:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")

        self.options.add_argument("--disable-blink-features=AutomationControlled")
        # self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-plugins")
        self.options.add_argument("--disable-images")  # Faster loading
        self.options.add_argument("--disable-css")  # Disable CSS for faster loading
        self.options.add_argument("--disable-fonts")  # Disable font loading
        self.options.add_argument("--disable-background-timer-throttling")
        self.options.add_argument("--disable-backgrounding-occluded-windows")
        self.options.add_argument("--disable-renderer-backgrounding")
        self.options.add_argument("--disable-features=TranslateUI")
        self.options.add_argument("--disable-ipc-flooding-protection")
        self.options.add_argument("--disable-default-apps")
        self.options.add_argument("--disable-sync")
        self.options.add_argument("--disable-translate")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-features=VizDisplayCompositor")

        if self.service:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
        else:
            self.driver = webdriver.Chrome(options=self.options)

        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        return None

    def _get_user_profile(self) -> str | None:
        return os.getenv("USER_PROFILE")

    def _init_chrome_debug(self) -> None:
        """Start debug chrome session with provide user data"""

        command = [
            self.chrome_exec_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir{self._get_user_profile()}",
        ]
        subprocess.Popen(command)
        time.sleep(2)
        return None

    def get_pages(self) -> None:
        logging.info("Starting Chrome debug")
        self._init_chrome_debug()
        tabs = self.driver.window_handles
        for tab in tabs:
            logging.info("%s", tab)

    def get_browser_cookies(self) -> None:
        """Get all cookies from browser session you can filter after that :D"""
        return None


if __name__ == "__main__":
    program = Program(existing_session=True)
    program.get_pages()
