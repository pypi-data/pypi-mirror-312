from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_driver(browser_name):
    """
    Devuelve un WebDriver remoto basado en el navegador especificado.
    """
    selenium_hub_url = "http://localhost:4444"  # Dirección de Selenium Grid

    if browser_name == "chrome":
        options = ChromeOptions()
        options.set_capability('se:name', 'chrome')
        options.set_capability('se:recordVideo', True)
        return webdriver.Remote(command_executor=selenium_hub_url, options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.set_capability('se:name', 'firefox')
        options.set_capability('se:recordVideo', True)
        return webdriver.Remote(command_executor=selenium_hub_url, options=options)

    elif browser_name == "edge":
        options = EdgeOptions()
        options.set_capability('se:name', 'edge')
        options.set_capability('se:recordVideo', True)
        return webdriver.Remote(command_executor=selenium_hub_url, options=options)

    else:
        raise ValueError(f"El navegador '{browser_name}' no está soportado")
