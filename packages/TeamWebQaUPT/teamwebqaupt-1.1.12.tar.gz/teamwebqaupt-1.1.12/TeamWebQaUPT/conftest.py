import pytest
from TeamWebQaUPT.webdriver_config import get_driver

@pytest.fixture(scope="session")
def driver(request):
    browser_name = request.param
    driver = get_driver(browser_name)
    driver.maximize_window()
    yield driver
    driver.quit()
