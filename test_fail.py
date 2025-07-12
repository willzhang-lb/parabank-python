def test_fail(page):
    page.goto("https://example.com")
    assert False, "Force failure to trigger trace"