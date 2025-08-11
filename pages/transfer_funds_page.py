from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class TransferFundsPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)

    def transfer_fund(self, first_account: str = '', second_account: str = '', transfer_amount: str = '0.01'):
        self.from_account_dropdown = self.right_panel.locator('#fromAccountId')
        self.to_account_dropdown = self.right_panel.locator('#toAccountId')

        # Select value for from_account_dropdown
        if first_account:
            self.from_account_dropdown.select_option(first_account)
        else:
            self.from_account_dropdown.select_option(index=0)

        # Get the selected value from from_account_dropdown
        first_account_id = self.from_account_dropdown.locator('option[selected="selected"]').text_content().strip()

        # Get all options from to_account_dropdown
        to_account_id_list = [
            self.to_account_dropdown.locator('option').nth(i).text_content().strip()
            for i in range(self.to_account_dropdown.locator('option').count())
        ]

        # Select a value for to_account_dropdown that is different from first_account_id
        if second_account and second_account != first_account_id:
            self.to_account_dropdown.select_option(second_account)
        else:
            for account_id in to_account_id_list:
                if account_id != first_account_id:
                    self.to_account_dropdown.select_option(account_id)
                    break

        self.right_panel.locator('#amount').fill(transfer_amount)
        with self.page.expect_response('**/transfer**') as response_info:
            self.right_panel.locator('input[value="Transfer"]').click()
        self.page.wait_for_selector('#amount', state="hidden")