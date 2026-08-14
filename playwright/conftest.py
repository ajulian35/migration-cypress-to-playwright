import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

# PRE-001 (Admin creates employee) and PRE-002 (new user creates claim) must run first
_TEST_ORDER = [
    "pre_001", "pre_002", "req_003", "req_004", "req_001", "req_002", "req_006", "req_007"
]

def pytest_collection_modifyitems(items):
    def sort_key(item):
        for i, prefix in enumerate(_TEST_ORDER):
            if prefix in item.nodeid:
                return i
        return len(_TEST_ORDER)
    items.sort(key=sort_key)


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def browser_context(browser_instance):
    context = browser_instance.new_context(viewport={"width": 1280, "height": 720})
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def runtime_data():
    """Mutable store for values generated during the run (e.g. emp_number from pre_001)."""
    return {}

@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL", "https://opensource-demo.orangehrmlive.com")

@pytest.fixture(scope="session")
def credentials():
    """Admin credentials — used by req_002, req_005."""
    return {
        "username": os.environ.get("TEST_USER_EMAIL", "Admin"),
        "password": os.environ.get("TEST_USER_PASSWORD", "admin123"),
    }

@pytest.fixture(scope="session")
def new_user_credentials():
    """New employee credentials created in pre_001 — used by req_001, req_002, req_003, req_004, req_006, req_007."""
    return {
        "username": os.environ.get("NEW_USER_EMAIL", "qauser_001"),
        "password": os.environ.get("NEW_USER_PASSWORD", "QAuser123!"),
        "emp_number": os.environ.get("NEW_EMP_NUMBER", "209"),
        "emp_id": os.environ.get("NEW_EMP_ID", "0384"),
        "claim_ref_id": os.environ.get("CLAIM_REF_ID", "202608070000008"),
    }
