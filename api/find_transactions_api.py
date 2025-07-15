import os
from .base_api import BaseAPI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv('BASE_URL')


class TransactionsAPI(BaseAPI):
    def get_transactions_by_amount(self, account_id, amount):
        url = f"{BASE_URL}/services_proxy/bank/accounts/{account_id}/transactions/amount/{amount}?timeout=30000"
        return self.request_context.get(url)
