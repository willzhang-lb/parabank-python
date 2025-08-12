import os
from dotenv import load_dotenv



class BaseAPI:
    def __init__(self, request_context, env_config):
        self.request_context = request_context
        self.base_url = env_config['Baseurl']