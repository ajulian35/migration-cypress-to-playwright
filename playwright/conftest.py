import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        yield context
        browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL", "https://opensource-demo.orangehrmlive.com")

@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.environ.get("TEST_USER_EMAIL", "Admin"),
        "password": os.environ.get("TEST_USER_PASSWORD", "admin123"),
    }
