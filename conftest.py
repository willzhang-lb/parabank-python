import json
import logging
import os
from pathlib import Path

import pytest
from playwright.sync_api import expect, Playwright


from utils import load_json_file_info

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
STORAGE_PATH = os.path.join(os.path.dirname(__file__), "member_storage.json")

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment: dev, qa, prod"
    )

@pytest.fixture(scope="session", autouse=True)
def get_env(request):
    env_value = request.config.getoption("--env")
    if env_value not in ["dev", "qa", "prod"]:
        raise ValueError("Invalid environment value")

    return env_value

@pytest.fixture(scope="session")
def env_config(request, get_env):
    # get config file from different env
    with open(f'config/{get_env}_config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# Hook to capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)


@pytest.fixture(scope="function", autouse=True)
def member_storage(context, env_config):
    """Ensure valid member_storage.json exists"""
    base_url = env_config['Baseurl']
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
def api_request_context(playwright: Playwright, env_config):
    base_url = env_config['Baseurl']
    extra_headers = {}

    storage = load_json_file_info('member_storage.json')
    cookies = storage.get("cookies", [])
    print(cookies)
    extra_headers["Cookie"] = cookies[0]['name'] + '=' + cookies[0]['value']
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers=extra_headers,
        ignore_https_errors=True,
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
def page(context, env_config):
    base_url = env_config['Baseurl']
    page = context.new_page()
    page.goto(base_url)
    yield page
    page.close()


# def pytest_addoption(parser):
#     parser.addoption("--envfile", action="store", default=".env", help="Environment file to load")
#
#
# def pytest_configure(config):
#     envfile = config.getoption("envfile")
#     load_dotenv(dotenv_path=envfile)
#     # global BASE_URL
#     # BASE_URL = os.getenv('BASE_URL')
