
from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info



class RegisterPage(BasePage):
    def __init__(self, page, env_config):
        super().__init__(page, env_config)
        page.goto(f"{self.base_url}/register.htm")

    def fill_register_info(self):
        dump_to_json('data/member_info.json', 'Username', self.random_username)
        member_info = load_json_file_info('data/member_info.json')
        self.page.wait_for_selector('h1:has-text("Signing up is easy!")', state="visible")
        self.fill_form(member_info)
        self.click_button('Register')

    def click_register(self):
        self.left_panel.get_by_text('Register').click()

    def verify_register_success(self):
        # Verify that the registration was successful
        success_message = self.right_panel.locator('.title').text_content()
        expected_title = "Welcome " + self.random_username
        assert success_message == expected_title, f"Welcome message {success_message} does not match expected title '{expected_title}'"