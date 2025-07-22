from api.find_transactions_api import TransactionsAPI
from utils import load_json_file_info

new_account = load_json_file_info('data/account_info.json')['new account']

def test_get_transactions(api_request_context):
    # Call the API endpoint
    tx_api = TransactionsAPI(api_request_context)
    response = tx_api.get_transactions_by_amount(account_id=new_account, amount=1)
    body = response.json()
    # Basic asserts
    assert response.status == 200
    for i in range(len(body)):
        assert float(body[i]['amount']) == 1.0, f"Expected amount to be 1.0, but got {body[i]['amount']}"