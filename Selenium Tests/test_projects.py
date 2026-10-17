"""Gallery interaction and project detail modal tests."""

from urllib.parse import urljoin
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_project_click_opens_modal_and_escape_closes(load_home, driver, base_url):
    """TC-04: A gallery card opens a modal, and Escape returns home."""
    driver.set_window_size(390, 844)  # Avoid desktop-only pinned horizontal scroll.
    load_home()
    card = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#project-1[role="button"]'))
    )
    card.click()
    WebDriverWait(driver, 15).until(lambda d: "/projects/diabetes-classification" in d.current_url)
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-lenis-prevent]'))
    )
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    WebDriverWait(driver, 15).until(lambda d: d.current_url.rstrip("/") == base_url.rstrip("/"))
    WebDriverWait(driver, 15).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '[data-lenis-prevent]'))
    )


def test_project_card_supports_enter(load_home, driver):
    """TC-12: Keyboard users can open a project card using Enter."""
    driver.set_window_size(390, 844)
    load_home()
    card = driver.find_element(By.ID, "project-1")
    card.send_keys(Keys.ENTER)
    WebDriverWait(driver, 15).until(lambda d: "/projects/diabetes-classification" in d.current_url)


@pytest.mark.xfail(reason="Potential direct-link defect: App.jsx only declares '/' in the main Routes.", strict=False)
def test_direct_project_url_can_load_without_prior_navigation(driver, base_url):
    """TC-13 (exploratory): Deep-linking to a project ought to render its details."""
    driver.get(urljoin(base_url, "projects/diabetes-classification"))
    WebDriverWait(driver, 10).until(
        lambda d: "Diabetes Classification" in d.find_element(By.TAG_NAME, "body").text
    )
