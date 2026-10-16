import pytest

pytestmark = pytest.mark.responsive

VIEWPORTS = {
    "mobile": (375, 667),
    "tablet": (768, 1024),
    "laptop": (1366, 768),
    "desktop": (1920, 1080),
}


@pytest.mark.parametrize("name,size", VIEWPORTS.items())
def test_no_horizontal_scroll(driver, base_url, name, size):
    driver.set_window_size(*size)
    driver.get(base_url)
    overflow = driver.execute_script(
        "return document.documentElement.scrollWidth - document.documentElement.clientWidth;"
    )
    assert overflow <= 1, f"{name} ({size[0]}px): page overflows horizontally by {overflow}px"


def test_viewport_meta_tag_present(home):
    assert home.execute_script(
        "return !!document.querySelector('meta[name=viewport]');"
    ), "Missing <meta name='viewport'> tag"