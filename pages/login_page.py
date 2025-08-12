from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info

class LoginPage(BasePage):
    def __init__(self, page, env_config):
        super().__init__(page, env_config)


    def login(self):
        member_info = load_json_file_info('data/member_info.json')
        self.left_panel.locator('input[name="username"]').fill(member_info['Username'])
        self.left_panel.locator('input[name="password"]').fill(member_info['Password'])
        self.click_button('Log In')