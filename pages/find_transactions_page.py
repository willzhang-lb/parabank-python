from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class FindTransactionsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def find_transaction_by_category(self, category, first_value: str, second_value: str = ''):
        """
        Find a transaction by category and value.
        :param second_value:
        :param first_value:
        :param category: The category to search for.
        :return: The transaction row if found, None otherwise.
        """
        global index
        if category == 'transaction_id':
            self.right_panel.locator('#transactionId').fill(first_value)
            index = 0
        elif category == 'transaction_date':
            self.right_panel.locator('#transactionDate').fill(second_value)
            index = 1
        elif category == 'transaction_date_range':
            self.right_panel.locator('#fromDate').fill(first_value)
            self.right_panel.locator('#toDate').fill(second_value)
            index = 2
        elif category == 'transaction_amount':
            self.right_panel.locator('#amount').fill(first_value)
            index = 3

        with self.page.expect_response('**/transactions/**') as response_info:
            self.right_panel.locator('#transactionForm').get_by_text('Find Transactions').nth(index).click()

        self.right_panel.get_by_role('button', name='Find Transactions').first.wait_for(state="hidden")
        print(response_info)
        print(response_info.value)