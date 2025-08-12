from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class BillPayPage(BasePage):
    def __init__(self, page, env_config):
        super().__init__(page, env_config)

    def fill_bill_info(self):
        bill_info = load_json_file_info('data/bill_info.json')
        account_info = load_json_file_info('data/account_info.json')
        bill_info['From account'] = account_info['New Account']
        self.page.wait_for_selector('h1:has-text("Bill Payment Service")', state="visible")
        self.fill_form(bill_info)
        self.click_button('Send Payment')
        self.page.wait_for_selector('input[value="Send Payment"]', state="hidden")