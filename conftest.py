import json
import logging
import os
import time

import playwright
import pytest

import allure
import pytest
from playwright.sync_api import expect, Playwright
from test import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# @pytest.fixture(scope="module")
# def member_storage_state(playwright, timeout):
#     headers = {"Accept": "application/prs.CRM-Back-End.v2+json"}
#     request_context = playwright.request.new_context(base_url=api_url, extra_http_headers=headers, ignore_https_errors=True)
#     data = {"username": user_email, "password": user_password}
#
#     response = request_context.post('/api/authorizations/member', data=data, timeout=timeout)
#
#     response_json = response.json()
#
#     assert response.ok, 'The Login request is fail.'
#     assert response_json.get('access_token'), f'The member cannot login successfully, {response_json}'
#
#     token = response_json.get('access_token')
#     state = request_context.storage_state()
#     member_token = json.dumps(
#         {"access_token": token, "countDownModalShowExpire": expire-10000, "expire": expire,
#          "needShowExpireModal": "true", "session_duration": 900})
#     state['origins'] = [{"origin": home_page_url, "localStorage": [{"name": "member_token", "value": member_token}]}]
#     return state

# Hook to capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)

@pytest.fixture(scope='function')
def authed_context(playwright, request):
    # Launch browser in headed mode
    browser = playwright.chromium.launch(headless=False, args=["--start-fullscreen"])
    context = browser.new_context()

    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

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
    browser.close()

@pytest.fixture(scope='function')
def page(authed_context):
    page = authed_context.new_page()
    yield page
    page.close()

