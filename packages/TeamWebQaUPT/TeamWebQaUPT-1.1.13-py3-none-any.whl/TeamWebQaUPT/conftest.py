import pytest
from TeamWebQaUPT.webdriver_config import get_driver

@pytest.fixture(scope="function", params=["chrome", "firefox", "edge"])
def driver(request):
    """
    Crea un WebDriver remoto basado en el navegador especificado.
    """
    browser_name = request.param
    driver = get_driver(browser_name)  
    driver.maximize_window()
    yield driver
    driver.quit()
