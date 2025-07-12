from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info

member_info = load_json_file_info('member_info.json')

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.new_account_id = None

    def verify_register_function(self):
        self.click_register()
        self.fill_register_info()
        self.verify_register_success()

    def verify_open_new_account_function(self):
        self.click_left_menu('Open New Account')
        self.verify_title_correct('Open New Account')
        self.open_new_account()
        self.verify_title_correct('Account Opened!')
        self.save_new_account_number()

    def verify_transfer_fund_function(self):
        account_info = load_json_file_info('account_info.json')
        from_account = account_info['new account']
        self.click_left_menu('Transfer Funds')
        self.verify_title_correct('Transfer Funds')
        self.transfer_fund(first_account=from_account, transfer_amount='1')
        self.verify_title_correct('Transfer Complete!')

    def verify_bill_pay_function(self):
        self.click_left_menu('Bill Pay')
        self.verify_title_correct('Bill Payment Service')
        self.fill_bill_info()
        self.verify_title_correct('Bill Payment Complete')

    def verify_find_transactions_function(self):
        self.click_left_menu('Find Transactions')
        self.verify_title_correct('Find Transactions')
        self.find_transaction_by_category('transaction_amount', '1')
        self.verify_title_correct('Transaction Results')

