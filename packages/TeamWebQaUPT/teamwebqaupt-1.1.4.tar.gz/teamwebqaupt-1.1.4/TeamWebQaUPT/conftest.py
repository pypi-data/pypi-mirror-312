import pytest
from TeamWebQaUPT.webdriver_config import get_driver

@pytest.fixture(scope="session", params=["chrome", "firefox", "edge"])
def driver(request):
    """
    Fixture para inicializar navegadores en Selenium Grid.
    """
    browser = request.param
    driver = get_driver(browser)
    driver.maximize_window()
    yield driver
    driver.quit()
