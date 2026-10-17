"""Reuse stable aria-labels and roles instead of styling classes."""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WAIT_SECONDS = 15


def open_terminal(driver):
    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Open terminal (Ctrl+K)"]'))
    ).click()
    return WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Terminal input"]'))
    )


def terminal_command(driver, command, expected):
    field = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-label="Terminal input"]'))
    )
    field.send_keys(command, Keys.ENTER)
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: expected in d.find_element(By.CSS_SELECTOR, '[role="log"][aria-label="Chat messages"]').text
    )
    return driver.find_element(By.CSS_SELECTOR, '[role="log"][aria-label="Chat messages"]').text


def section_near_top(driver, section_id, tolerance=190):
    """Scroll happens asynchronously through Lenis; do not assert immediately."""
    def near_top(d):
        top = d.execute_script(
            "return document.getElementById(arguments[0]).getBoundingClientRect().top",
            section_id,
        )
        return abs(top) <= tolerance
    return WebDriverWait(driver, WAIT_SECONDS).until(near_top)
