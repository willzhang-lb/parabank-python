import json
import logging
import os
from datetime import datetime

import playwright
import pytest
from playwright.async_api import async_playwright
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


@pytest.fixture(scope="function", autouse=True)
def member_storage(context):
    """Ensure valid member_storage.json exists"""
    member_info = load_json_file_info("data/member_info.json")
    page = context.new_page()
    page.goto(f"{BASE_URL}/overview.htm")
    if page.locator('//h1[contains(text(), "Accounts Overview")]').is_visible():
        logging.info("Valid session found, skipping login.")
        return
    else:
        page.locator('input[name="username"]').fill(member_info['Username'])
        page.locator('input[name="password"]').fill(member_info['Password'])
        page.locator('input[value="Log In"]').click()
        context.storage_state(path=STORAGE_PATH)
        page.close()


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    extra_headers = {}

    storage = json.loads(Path(STORAGE_PATH).read_text())
    cookies = storage.get("cookies", [])

    extra_headers["Cookie"] = cookies[0]['name'] + '=' + cookies[0]['value']
    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers=extra_headers,
        ignore_https_errors=True
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session")
async def playwright_instance():
    async with async_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright):
    is_ci = os.getenv("CI", "false").lower() == "true"
    browser = playwright.chromium.launch(headless=is_ci)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, request):
    context = browser.new_context(storage_state=STORAGE_PATH)

    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context



    # Create trace directory
    trace_folder = os.path.join(os.getcwd(), 'trace')
    os.makedirs(trace_folder, exist_ok=True)
    trace_file = os.path.join(trace_folder, f"trace_{request.node.name}.zip")

    try:
        # Get test outcome
        rep = getattr(request.node, "rep_call", None)

        if rep and rep.failed:
            context.tracing.stop(path=trace_file)
        else:
            context.tracing.stop()
    except Exception as e:
        logging.error(f"Error while stopping tracing: {e}")
        # Ensure tracing is stopped even if an error occurs
        context.tracing.stop()
    finally:
        context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()

