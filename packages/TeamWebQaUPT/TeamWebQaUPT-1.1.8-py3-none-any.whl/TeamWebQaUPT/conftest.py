import pytest
from TeamWebQaUPT.webdriver_config import get_driver

@pytest.fixture(scope="function")
def driver(request):
    browser = request.param  
    driver = get_driver(browser)
    driver.maximize_window()
    yield driver
    driver.quit()

def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        metafunc.parametrize("driver", ["chrome", "firefox", "edge"], indirect=True)
