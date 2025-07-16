import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

base_url = os.getenv('BASE_URL')

class BaseAPI:
    def __init__(self, request_context):
        self.request_context = request_context
        self.base_url = base_url