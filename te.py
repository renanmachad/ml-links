from webdriver_manager.core.driver import Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from typing import Optional
import logging
from selenium.webdriver.chrome.options import Options


class Program:
    def __init__(self, existing_session=False):
        self.existing_session = existing_session
        self.options = Options()
        self.service: Optional[Service] = None
        self.driver: webdriver.Chrome
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
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
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

    def get_pages(self) -> None:
        tabs = self.driver.window_handles
        for tab in tabs:
            logging.info("%s", tab)


if __name__ == "__main__":
    program = Program(existing_session=True)
    program.get_pages
