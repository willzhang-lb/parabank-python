
from pages.home_page import HomePage



class TestEndToEnd:

    def test_e2e(self, page):
        home_page = HomePage(page)
        home_page.navigate_to_home_page()
        home_page.verify_register_function()
        home_page.verify_open_new_account_function()
        home_page.verify_transfer_fund_function()
        home_page.verify_bill_pay_function()
        home_page.verify_find_transactions_function()


