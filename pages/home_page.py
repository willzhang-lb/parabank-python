from pages.base_page import BasePage
from utils import generate_username, dump_to_json, load_json_file_info


class HomePage(BasePage):
    def __init__(self, page, env_config):
        super().__init__(page, env_config)
