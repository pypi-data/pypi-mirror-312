import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_driver(browser_name):
    """
    Devuelve una instancia de WebDriver remoto.
    """
    if browser_name == "chrome":
        options = ChromeOptions()
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=options
        )
    elif browser_name == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=options
        )
    elif browser_name == "edge":
        options = EdgeOptions()
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=options
        )
    else:
        raise ValueError(f"Navegador '{browser_name}' no es compatible.")
    
    driver.maximize_window()
    return driver

