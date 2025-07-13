from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class AccountOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def verify_account_balance(self, account_id: str, expected_balance_value: str):
        self.table = self.right_panel.locator('#accountTable')
        self.target_row = self.table.locator('tbody > tr').filter(has_text=account_id)
        balance_text = self.target_row.locator('td:nth-child(2)').text_content().replace("$", "").strip()
        assert float(balance_text) == float(
            expected_balance_value), f"Balance {balance_text} does not match expected value {expected_balance_value}"