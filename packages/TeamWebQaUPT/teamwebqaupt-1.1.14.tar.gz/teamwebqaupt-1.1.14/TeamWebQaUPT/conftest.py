import pytest
from webdriver_config import get_driver

@pytest.fixture(scope="session", params=["chrome", "firefox", "edge"])
def driver(request):
    """
    Fixture para inicializar un WebDriver remoto en Selenium Grid.
    """
    browser = request.param  # Usamos request.param para parametrizar el navegador
    driver = get_driver(browser)
    driver.maximize_window()
    yield driver
    driver.quit()
