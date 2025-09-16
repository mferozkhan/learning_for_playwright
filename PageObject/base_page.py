from playwright.sync_api import Page, expect
from Utilities.config_reader import ConfigReader
import os


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.config = ConfigReader()
        self.wait_time = self.config.get_wait_time()

    def goto(self, url):
        self.page.goto(url)

    def click(self, locator):
        self.page.click(locator)

    def fill(self, locator, text):
        self.page.fill(locator, text)

    def get_text(self, locator):
        return self.page.text_content(locator)

    def wait_for_element(self, locator):
        self.page.wait_for_selector(locator, timeout=self.wait_time * 1000)

    def take_screenshot(self, name):
        screenshot_dir = "Screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        self.page.screenshot(path=os.path.join(screenshot_dir, f"{name}.png"))

    def start_tracing(self, name):
        self.page.context.tracing.start(
            title=name,
            screenshots=True,
            snapshots=True,
            sources=True
        )

    def stop_tracing(self, name):
        result_dir = "Result"
        os.makedirs(result_dir, exist_ok=True)
        self.page.context.tracing.stop(path=os.path.join(result_dir, f"{name}.zip"))