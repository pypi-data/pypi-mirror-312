from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_driver(browser_name):
    if browser_name == "chrome":
        options = ChromeOptions()
        options.set_capability('se:name', 'chrome-tests')
        options.set_capability('se:recordVideo', True)
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=options
        )
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.set_capability('se:name', 'firefox-tests')
        options.set_capability('se:recordVideo', True)
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=options
        )
    elif browser_name == "edge":
        options = EdgeOptions()
        options.set_capability('se:name', 'edge-tests')
        options.set_capability('se:recordVideo', True)
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=options
        )
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported")
    return driver
