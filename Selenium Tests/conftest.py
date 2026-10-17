"""Shared Chrome WebDriver fixtures for the MotionFolio browser tests."""
from urllib.parse import urljoin

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        default="http://localhost:5173",
        help="URL of your locally running MotionFolio Vite server",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run Chrome without an on-screen browser (omit for video recording)",
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/") + "/"


@pytest.fixture
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--disable-notifications")
    # Selenium 4.6+ uses Selenium Manager for browser driver resolution.
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1440, 900)
    browser.set_page_load_timeout(40)
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def load_home(driver, base_url):
    """Return a helper to open the portfolio after optional viewport setup."""
    def _load():
        driver.get(urljoin(base_url, ""))
        wait = WebDriverWait(driver, 40)
        # App initially shows an animated preloader with scroll locked.
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        wait.until(lambda d: bool(d.find_elements(By.CSS_SELECTOR, "#project-section .project-card")))
        wait.until(lambda d: not d.find_elements(By.CSS_SELECTOR, '[class*="z-[9999]"]'))
        return driver
    return _load
