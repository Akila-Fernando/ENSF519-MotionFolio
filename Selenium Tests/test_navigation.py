"""Desktop and mobile navigation behavior."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.helpers import section_near_top


def test_desktop_about_navigation(load_home, driver):
    """TC-02: About should scroll to the about-section anchor."""
    load_home()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//nav//button[.//span[normalize-space()="About"]]'))
    ).click()
    assert section_near_top(driver, "about-section")


def test_mobile_menu_navigation(load_home, driver):
    """TC-05: The mobile menu should open, navigate to Logs, and close."""
    driver.set_window_size(390, 844)
    load_home()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'nav button[aria-label="Open menu"]'))
    ).click()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//nav//button[.//span[normalize-space()="Logs"]]'))
    ).click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'nav button[aria-label="Open menu"]'))
    )
    assert section_near_top(driver, "project-section")
