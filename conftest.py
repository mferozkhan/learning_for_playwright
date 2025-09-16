import pytest
import os
import shutil
import asyncio
from Utilities.custom_logger import Logger

# Initialize logger globally
log = Logger().get_logger()
log.info("🚀 Playwright test execution started.")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chromium",
                     help="Browser to use (chromium, firefox, webkit)")
    parser.addoption("--view", action="store", default="desktop",
                     help="View mode (mobile or desktop)")
    parser.addoption("--headless", action="store", default="false",
                     help="Run in headless mode (true or false)")


# ========== Return selected browser ==========
@pytest.fixture()
def browser_name(request):
    return request.config.getoption('--browser')


# ========== Return headless option ==========
@pytest.fixture()
def is_headless(request):
    return request.config.getoption('--headless').lower() == 'true'


# ========== Return view mode ==========
@pytest.fixture()
def view_mode(request):
    return request.config.getoption('--view')


# ========== Playwright Browser setup fixture ==========
@pytest.fixture(scope="function")
def playwright_browser(request, browser_name, is_headless, view_mode):
    from playwright.sync_api import sync_playwright

    # Set up download directory
    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    # Clean download directory
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"⚠️ Failed to delete {file_path}. Reason: {e}")

    # Launch Playwright - use a new event loop to avoid asyncio conflicts
    with sync_playwright() as playwright:
        # Browser launch options with downloads path
        launch_options = {
            "headless": is_headless,
            "slow_mo": 500,
            "downloads_path": download_dir
        }

        # Select browser type
        if browser_name.lower() == 'chromium':
            browser_instance = playwright.chromium.launch(**launch_options)
        elif browser_name.lower() == 'firefox':
            browser_instance = playwright.firefox.launch(**launch_options)
        elif browser_name.lower() == 'webkit':
            browser_instance = playwright.webkit.launch(**launch_options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}. Choose from chromium, firefox, webkit.")

        # Context options
        context_options = {
            "accept_downloads": True,
        }

        # Set viewport for mobile/desktop
        if view_mode.lower() == "mobile":
            context_options["viewport"] = {"width": 390, "height": 844}
            context_options["user_agent"] = (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
            )
        else:
            context_options["viewport"] = {"width": 1366, "height": 768}

        # Create context
        context = browser_instance.new_context(**context_options)

        yield context

        # Cleanup
        context.close()
        browser_instance.close()


# ========== Page fixture ==========
@pytest.fixture()
def page(playwright_browser):
    page = playwright_browser.new_page()
    yield page
    page.close()


# ========== HTML Report Metadata ==========
def pytest_configure(config):
    config._metadata = {
        'Project Name': 'Playwright Automation Framework',
        'Module Name': 'Web Testing',
        'Tester': 'Automation Engineer',
        'Browser': config.getoption('--browser'),
        'View Mode': config.getoption('--view'),
        'Headless': config.getoption('--headless')
    }


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("plugins", None)