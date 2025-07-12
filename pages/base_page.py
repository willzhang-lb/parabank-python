import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from utils import generate_username, dump_to_json, load_json_file_info


random_username = generate_username()

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.left_panel = self.page.locator('#leftPanel')
        self.right_panel = self.page.locator('#rightPanel')
        self.random_username = generate_username()

    def navigate_to_home_page(self):
        load_dotenv()
        url = os.getenv('BASE_URL')  # Get the URL from the .env file
        if not url:
            raise ValueError("BASE_URL is not set in the .env file")
        self.page.goto(url)

    def login(self):
        member_info = load_json_file_info('member_info.json')
        self.left_panel.locator('input[name="username"]').fill(member_info['Username'])
        self.left_panel.locator('input[name="password"]').fill(member_info['Password'])
        self.click_button('Log In')

    def verify_title_correct(self, expected_title: str):

        title = self.get_visible_title()
        print(title)
        assert title == expected_title, f"Displayed title {title} does not match expected title '{expected_title}'"

    def get_visible_title(self):
        titles = self.right_panel.locator('.title')
        count = titles.count()

        for i in range(count):
            el = titles.nth(i)
            if el.is_visible():
                title = el.text_content().strip()
                return title

    def click_left_menu(self, menu_item: str):
        self.left_panel.get_by_text(menu_item).click()

    def click_register(self):
        self.left_panel.get_by_text('Register').click()

    def fill_register_info(self):
        dump_to_json('member_info.json', 'Username', self.random_username)
        member_info = load_json_file_info('member_info.json')
        self.page.wait_for_selector('h1:has-text("Signing up is easy!")', state="visible")
        self.fill_form(member_info)
        self.click_button('Register')

    def fill_form(self, form_data: dict):
        """
        Fill a form field with the given value.
        :param form_data:
        """
        self.page.wait_for_selector('#rightPanel table tbody')
        for key, value in form_data.items():
            row = self.right_panel.locator('tr').filter(has_text=key).first
            target_field = row.locator('td:nth-child(2) > *')
            if self.get_html_tag_of_node(target_field) == 'INPUT':
                target_field.fill(value)
            elif target_field.get_attribute('class') == 'SELECT':
                target_field.select_option(value)


    def click_button(self, button_text):
        """
        Click a button with the specified text.
        :param button_text: The text of the button to click.
        """
        button = self.page.locator(f'//input[@class="button" and @value="{button_text}"]')
        self.page.wait_for_selector(f'//input[@class="button" and @value="{button_text}"]', state="visible")
        if button.is_visible() and button.is_editable():
            button.click()
        else:
            raise ValueError(f"Button with text '{button_text}' is not visible on the page.")

    def fill_bill_info(self):
        bill_info = load_json_file_info('bill_info.json')
        account_info = load_json_file_info('account_info.json')
        bill_info['From account'] = account_info['new account']
        print(account_info)
        self.page.wait_for_selector('h1:has-text("Bill Payment Service")', state="visible")
        self.fill_form(bill_info)
        self.click_button('Send Payment')
        self.page.wait_for_selector('input[value="Send Payment"]', state="hidden")

    # Python
    def get_html_tag_of_node(self, locator) -> str:
        """
        Get the HTML tag of the node specified by the selector.
        :return: The HTML tag name of the node.
        """
        element_handle = locator
        if element_handle:
            return element_handle.evaluate("node => node.tagName")
        else:
            raise ValueError(f"No element found")

    def open_new_account(self, from_account: str = ''):

        self.right_panel.locator('#type').select_option('SAVINGS')
        if from_account:
            self.right_panel.locator('#fromAccountId').select_option(from_account)
        else:
            self.right_panel.locator('#fromAccountId').select_option(index=0)
        self.page.wait_for_selector('#fromAccountId option', state="attached")
        self.click_button('Open New Account')
        self.page.wait_for_selector('#openAccountResult')

    def verify_register_success(self):
        # Verify that the registration was successful
        success_message = self.right_panel.locator('.title').text_content()
        expected_title = "Welcome " + self.random_username
        assert success_message == expected_title, f"Welcome message {success_message} does not match expected title '{expected_title}'"

    def save_new_account_number(self):
        self.new_account_id = self.right_panel.locator('#newAccountId').text_content()
        dump_to_json('account_info.json', 'new account', self.new_account_id)
        return self.new_account_id

    def verify_new_account_balance(self, expected_balance_value: str):
        self.table = self.right_panel.locator('#accountTable')
        self.target_row = self.table.locator('tbody > tr').filter(has_text=self.new_account_id)
        balance_text = self.target_row.locator('td:nth-child(2)').text_content().replace("$", "").strip()
        print(balance_text)
        assert float(balance_text) == float(
            expected_balance_value), f"Balance {balance_text} does not match expected value {expected_balance_value}"

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
        print(response_info)
        print(response_info.value)

