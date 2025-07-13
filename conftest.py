import logging
import os
import playwright
import pytest
from playwright.sync_api import expect, Playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# Hook to capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)

@pytest.fixture(scope='function')
def context(playwright, request):
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
def page(context):
    page = context.new_page()
    yield page
    page.close()

