from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_driver(browser_name):
    selenium_hub_url = "http://localhost:4444"  # Cambia si tu Selenium Grid está en otro lugar.
    
    if browser_name == "chrome":
        options = ChromeOptions()
        driver = webdriver.Remote(command_executor=selenium_hub_url, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Remote(command_executor=selenium_hub_url, options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        driver = webdriver.Remote(command_executor=selenium_hub_url, options=options)
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported")
    
    return driver
