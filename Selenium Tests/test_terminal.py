"""Tests of the local, deterministic terminal commands: no API key needed."""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.helpers import open_terminal, terminal_command


def test_help_lists_commands(load_home, driver):
    """TC-06: The help command should list commands available to visitors."""
    load_home()
    open_terminal(driver)
    response = terminal_command(driver, "help", "AVAILABLE COMMANDS")
    assert "cat <id>" in response
    assert "history" in response


def test_ls_lists_projects(load_home, driver):
    """TC-07: The ls command should display the project inventory."""
    load_home()
    open_terminal(driver)
    response = terminal_command(driver, "ls", "Total: 8 projects")
    assert "diabetes-classification" in response
    assert "leadsup" in response


def test_cat_valid_project(load_home, driver):
    """TC-08: A known slug should show the project's details."""
    load_home()
    open_terminal(driver)
    response = terminal_command(driver, "cat diabetes-classification", "Diabetes Classification")
    assert "Category" in response
    assert "Stack" in response


def test_cat_invalid_project(load_home, driver):
    """TC-09: Invalid project slugs should yield a helpful error, not crash."""
    load_home()
    open_terminal(driver)
    response = terminal_command(driver, "cat no-such-project", "not found")
    assert "Available projects" in response


def test_clear_erases_terminal_log(load_home, driver):
    """TC-10: Clear removes previous messages from the terminal log."""
    load_home()
    open_terminal(driver)
    terminal_command(driver, "help", "AVAILABLE COMMANDS")
    field = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Terminal input"]')
    field.send_keys("clear", Keys.ENTER)
    WebDriverWait(driver, 15).until(
        lambda d: "AVAILABLE COMMANDS" not in d.find_element(
            By.CSS_SELECTOR, '[role="log"][aria-label="Chat messages"]'
        ).text
    )
    assert "AVAILABLE COMMANDS" not in driver.find_element(By.CSS_SELECTOR, '[role="log"]').text


def test_ctrl_k_opens_and_escape_closes_terminal(load_home, driver):
    """TC-11: The keyboard shortcut and Escape can control terminal visibility."""
    load_home()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("k").key_up(Keys.CONTROL).perform()
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Terminal input"]'))
    )
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    WebDriverWait(driver, 15).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Terminal input"]'))
    )
