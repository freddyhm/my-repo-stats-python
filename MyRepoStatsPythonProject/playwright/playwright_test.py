import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield browser, context
        context.close()
        browser.close()

@pytest.mark.usefixtures("browser")
def test_example(browser):
    browser, context = browser
    page = context.new_page()

    # Your Playwright test code here
    page.goto("https://example.com")
    assert page.title() == "Example Domain"

    # Close the page
    page.close()
