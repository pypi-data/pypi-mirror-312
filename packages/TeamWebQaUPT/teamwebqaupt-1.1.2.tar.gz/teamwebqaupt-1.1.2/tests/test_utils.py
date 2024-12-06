import pytest
from selenium import webdriver
from TeamWebQaUPT.utils import (
    select_dropdown_option,
    validate_elements_in_list,
    navigate_menu,
    navigate_linklabel,
)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_select_dropdown_option(driver):
    driver.get("https://example.com")
    select_dropdown_option(driver, "button[role='combobox']", "Option Text")
    selected_value = driver.find_element("css selector", "button[role='combobox']").text
    assert selected_value == "Option Text", f"Expected 'Option Text', got '{selected_value}'"

def test_validate_elements_in_list(driver):
    driver.get("https://example.com")
    validate_elements_in_list(driver, "//h3[contains(text(), '{}')]", ["Item 1", "Item 2"])
    assert driver.find_element("xpath", "//h3[contains(text(), 'Item 1')]").is_displayed()
    assert driver.find_element("xpath", "//h3[contains(text(), 'Item 2')]").is_displayed()

def test_navigate_menu(driver):
    driver.get("https://example.com")
    navigate_menu(
        driver,
        menu_items={"Home": "https://example.com/home"},
        base_url="https://example.com",
    )
    assert driver.current_url == "https://example.com/home", f"Expected URL 'https://example.com/home', got '{driver.current_url}'"

def test_navigate_linklabel(driver):
    driver.get("https://example.com")
    navigate_linklabel(driver, "a[data-testid='link']", "https://example.com/target")
    assert driver.current_url == "https://example.com/target", f"Expected URL 'https://example.com/target', got '{driver.current_url}'"
