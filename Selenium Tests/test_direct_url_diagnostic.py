
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def test_direct_url_refresh_diagnostic(driver, base_url):
    url = base_url.rstrip("/") + "/projects/diabetes-classification"

    def check_project_loaded():
        try:
            WebDriverWait(driver, 10).until(
                lambda d: "Diabetes Classification"
                in d.find_element(By.TAG_NAME, "body").text
            )
            return True
        except TimeoutException:
            return False

    driver.get(url)

    print("Initial load:", check_project_loaded())
    print("Initial history state:",
          driver.execute_script("return window.history.state"))
    driver.save_screenshot("tc13_initial.png")

    driver.refresh()

    print("After refresh:", check_project_loaded())
    print("Refreshed history state:",
          driver.execute_script("return window.history.state"))
    driver.save_screenshot("tc13_refreshed.png")
