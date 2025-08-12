
from .base_api import BaseAPI


class TransactionsAPI(BaseAPI):
    def __init__(self, request_context, env_config):
        super().__init__(request_context, env_config)

    def get_transactions_by_amount(self, account_id, amount):
        url = f"{self.base_url}/services_proxy/bank/accounts/{account_id}/transactions/amount/{amount}?timeout=30000"
        return self.request_context.get(url)
