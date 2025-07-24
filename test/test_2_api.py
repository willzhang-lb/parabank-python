from api.find_transactions_api import TransactionsAPI
from utils import load_json_file_info

account_info = load_json_file_info('data/account_info.json')
new_account = account_info['new account']

def test_get_transactions(api_request_context):
    # Call the API endpoint
    tx_api = TransactionsAPI(api_request_context)
    response = tx_api.get_transactions_by_amount(account_id=new_account, amount=1)
    print("Status:", response.status)
    print("Content-Type:", response.headers.get("content-type"))
    print("Response Text Preview:", response.text()[:200])  # Print first 200 characters

    assert response.ok, f"API call failed with status {response.status}"

    # Check if it's JSON before parsing
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type, "Response is not JSON"

    body = response.json()
    # Basic asserts
    assert response.status == 200
    for i in range(len(body)):
        assert float(body[i]['amount']) == 1.0, f"Expected amount to be 1.0, but got {body[i]['amount']}"