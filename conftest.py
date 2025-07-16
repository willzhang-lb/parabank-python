import json
import logging
import os
import playwright
import pytest
from playwright.sync_api import expect, Playwright, sync_playwright
from dotenv import load_dotenv
from pathlib import Path
# Load environment variables from .env file
load_dotenv()

from utils import load_json_file_info

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = os.getenv('BASE_URL')
STORAGE_PATH = "member_storage.json"

# Hook to capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)

def perform_login_and_save(context):
    member_info = load_json_file_info('member_info.json')
    page = context.new_page()
    page.goto(f"{BASE_URL}/overview.htm")
    page.locator('input[name="username"]').fill(member_info['Username'])
    page.locator('input[name="password"]').fill(member_info['Password'])
    page.locator('input[value="Log In"]').click()
    context.storage_state(path=STORAGE_PATH)
    page.close()


def is_logged_in(context) -> bool:
    page = context.new_page()
    page.goto(f"{BASE_URL}/overview.htm")
    result = not page.url.startswith(f"{BASE_URL}/overview")
    page.close()
    return result

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    extra_headers = {}

    if Path(STORAGE_PATH).exists():
        storage = json.loads(Path(STORAGE_PATH).read_text())
        cookies = storage.get("cookies", [])
        cookie_list = []
        for c in cookies:
            if c["domain"].endswith("parabank.parasoft.com"):
                cookie_list.append(f"{c['name']}={c['value']}")
        if cookie_list:
            extra_headers["Cookie"] = "; ".join(cookie_list)
    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers=extra_headers,
        ignore_https_errors=True
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def context(browser, request):
    context = None

    if os.path.exists(STORAGE_PATH):
        # Try using the existing session
        context = browser.new_context(storage_state=STORAGE_PATH)
        if not is_logged_in(context):
            print("[INFO] Stored session expired. Re-logging in.")
            context.close()
            context = browser.new_context()
            perform_login_and_save(context)
    else:
        # No session exists, perform login
        context = browser.new_context()
        perform_login_and_save(context)

    yield context
    # Get test outcome
    rep = getattr(request.node, "rep_call", None)

    # Create trace directory
    trace_folder = os.path.join(os.getcwd(), 'trace')
    os.makedirs(trace_folder, exist_ok=True)
    trace_file = os.path.join(trace_folder, f"trace_{request.node.name}.zip")

    if rep and rep.failed:
        logging.info("Test failed. Saving trace file...")
        context.tracing.stop(path=trace_file)
        logging.info(f"Trace file saved at: {trace_file}")
    else:
        context.tracing.stop()
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()


