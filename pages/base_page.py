import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from utils import generate_username, get_html_tag_of_node

load_dotenv()
random_username = generate_username()

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.left_panel = self.page.locator('#leftPanel')
        self.right_panel = self.page.locator('#rightPanel')
        self.random_username = generate_username()
        self.base_url = os.getenv('BASE_URL')

    def navigate_to_home_page(self):

        if not self.base_url:
            raise ValueError("BASE_URL is not set in the .env file")
        self.page.goto(self.base_url)

    def verify_title_correct(self, expected_title: str):

        title = self.get_visible_title()
        print(title)
        assert title == expected_title, f"Displayed title {title} does not match expected title '{expected_title}'"

    def get_visible_title(self):
        self.page.wait_for_selector('#rightPanel', state='visible')
        titles = self.right_panel.locator('.title')
        count = titles.count()

        for i in range(count):
            el = titles.nth(i)
            if el.is_visible():
                title = el.text_content().strip()
                return title

    def click_left_menu(self, menu_item: str):
        self.left_panel.get_by_text(menu_item).click()


    def fill_form(self, form_data: dict):
        """
        Fill a form field with the given value.
        :param form_data:
        """
        self.page.wait_for_selector('#rightPanel table tbody')
        for key, value in form_data.items():
            row = self.right_panel.locator('tr').filter(has_text=key).first
            target_field = row.locator('td:nth-child(2) > *')
            if get_html_tag_of_node(target_field) == 'INPUT':
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






