from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class OpenAccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

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
        dump_to_json('account_info.json', 'new account', self.new_account_id)
        return self.new_account_id