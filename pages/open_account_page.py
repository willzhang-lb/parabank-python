import re

from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class OpenAccountPage(BasePage):
    def __init__(self, page, env_config):
        super().__init__(page, env_config)

    def open_new_account(self, from_account: str = ''):
        self.right_panel.locator('#type').select_option('SAVINGS')
        if from_account:
            self.right_panel.locator('#fromAccountId').select_option(from_account)
        else:
            self.right_panel.locator('#fromAccountId').select_option(index=0)
        self.page.wait_for_selector('#fromAccountId option', state="attached")
        self.click_button('Open New Account')
        self.page.wait_for_selector('#openAccountResult')

    def save_new_account_number(self):
        self.new_account_id = self.right_panel.locator('#newAccountId').text_content()
        dump_to_json('data/account_info.json', 'New Account', self.new_account_id)
        return self.new_account_id

    def get_new_account_balance(self):
        balance_text = self.right_panel.locator('p:below(#type)').text_content()
        # Regular expression to match a monetary value

        match = re.search(r"\$([\d,]+(?:\.\d{2})?)", balance_text)
        if match:
            # Remove commas and convert to float
            amount_str = match.group(1).replace(',', '')
            return float(amount_str)
        else:
            print("No monetary value found.")