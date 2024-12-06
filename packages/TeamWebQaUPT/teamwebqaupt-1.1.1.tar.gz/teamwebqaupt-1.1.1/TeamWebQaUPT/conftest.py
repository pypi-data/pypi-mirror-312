import pytest
from webdriver_config import get_driver

# Fixture para parametrizar el navegador
@pytest.fixture(scope="session", params=["chrome", "firefox", "edge"])
def driver(request):
    browser = request.param  # Usamos request.param para obtener el navegador actual
    driver = get_driver(browser)
    driver.maximize_window()
    yield driver
    driver.quit()

