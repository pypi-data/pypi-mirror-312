from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_driver(browser_name):
    """
    Obtiene el driver remoto configurado para Selenium Grid.
    """
    selenium_grid_url = 'http://localhost:4444'

    if browser_name == "chrome":
        options = ChromeOptions()
        options.set_capability("browserName", "chrome")
        driver = webdriver.Remote(
            command_executor=selenium_grid_url,
            options=options
        )
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.set_capability("browserName", "firefox")
        driver = webdriver.Remote(
            command_executor=selenium_grid_url,
            options=options
        )
    elif browser_name == "edge":
        options = EdgeOptions()
        options.set_capability("browserName", "MicrosoftEdge")
        driver = webdriver.Remote(
            command_executor=selenium_grid_url,
            options=options
        )
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported for Selenium Grid")
    return driver
