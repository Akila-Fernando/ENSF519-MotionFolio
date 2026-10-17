"""Home page, sections, and gallery smoke tests."""
from selenium.webdriver.common.by import By


def test_home_loads_and_has_expected_sections(load_home, driver, base_url):
    """TC-01: A normal load should render the main portfolio sections."""
    load_home()
    assert driver.current_url.rstrip("/") == base_url.rstrip("/")
    for section_id in ("about-section", "project-section", "experience-section", "contact-section"):
        assert driver.find_element(By.ID, section_id).is_enabled()


def test_gallery_lists_eight_projects(load_home, driver):
    """TC-03: Eight gallery cards exist, matching src/data/projectMeta.js."""
    load_home()
    cards = driver.find_elements(By.CSS_SELECTOR, "#project-section .project-card")
    assert len(cards) == 8
    first_title = cards[0].find_element(By.TAG_NAME, "h3").text
    assert "DIABETES CLASSIFICATION" in first_title.upper()
