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
# BASE_URL = os.getenv('BASE_URL')
STORAGE_PATH = os.path.join(os.path.dirname(__file__), "member_storage.json")

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against: dev/staging/prod"
    )

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def base_url(env):
    env_map = {
        "qa": "https://parabank.parasoft.com/parabank",
        "staging": "https://google.com",
        "prod": "https://example.com"
    }
    return env_map.get(env, "https://parabank.parasoft.com/parabank")

# Hook to capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)


@pytest.fixture(scope="function", autouse=True)
def member_storage(context, base_url):
    """Ensure valid member_storage.json exists"""
    member_info = load_json_file_info("data/member_info.json")
    page = context.new_page()
    page.goto(f"{base_url}/overview.htm")
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
def api_request_context(playwright: Playwright, base_url):
    extra_headers = {}

    storage = json.loads(Path(STORAGE_PATH).read_text())
    cookies = storage.get("cookies", [])

    extra_headers["Cookie"] = cookies[0]['name'] + '=' + cookies[0]['value']
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers=extra_headers,
        ignore_https_errors=True
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def browser(playwright):
    is_ci = os.getenv("CI", "false").lower() == "true"
    browser = playwright.chromium.launch(headless=is_ci,
                                         args=["--disable-gpu", "--no-sandbox"]  )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, request):
    context = browser.new_context(storage_state=STORAGE_PATH)

    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Create trace directory
    trace_folder = os.path.join(os.path.dirname(__file__), "trace/")
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
def page(context, base_url):
    page = context.new_page()
    page.goto(base_url)
    yield page
    page.close()



