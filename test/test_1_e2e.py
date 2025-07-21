from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.bill_pay_page import BillPayPage
from pages.open_account_page import OpenAccountPage
from pages.transfer_funds_page import TransferFundsPage
from pages.account_overview_page import AccountOverviewPage
from pages.find_transactions_page import FindTransactionsPage

new_account = ''
transfer_amount = '1'

# # since login in function of parabank always fails, so I merge tests into one test file
# def test_e2e(page):
#     home_page = HomePage(page)
#     login_page = LoginPage(page)
#     register_page = RegisterPage(page)
#     bill_pay_page = BillPayPage(page)
#     open_account_page = OpenAccountPage(page)
#     transfer_funds_page = TransferFundsPage(page)
#     account_overview_page = AccountOverviewPage(page)
#     find_transactions_page = FindTransactionsPage(page)
#
#     register_page.fill_register_info()
#     register_page.verify_register_success()
#     home_page.click_left_menu('Open New Account')
#     open_account_page.verify_title_correct('Open New Account')
#     new_account_balance = open_account_page.get_new_account_balance()
#     open_account_page.open_new_account()
#     open_account_page.verify_title_correct('Account Opened!')
#     new_account = open_account_page.save_new_account_number()
#     home_page.click_left_menu('Accounts Overview')
#     account_overview_page.verify_title_correct('Accounts Overview')
#     account_overview_page.verify_account_balance(new_account, new_account_balance)
#
#     home_page.click_left_menu('Transfer Funds')
#     transfer_funds_page.verify_title_correct('Transfer Funds')
#     transfer_amount = '1'
#     transfer_funds_page.transfer_fund(first_account=new_account, transfer_amount=transfer_amount)
#     transfer_funds_page.verify_title_correct('Transfer Complete!')
#
#     home_page.click_left_menu('Bill Pay')
#     bill_pay_page.verify_title_correct('Bill Payment Service')
#     bill_pay_page.fill_bill_info()
#     bill_pay_page.verify_title_correct('Bill Payment Complete')
#
#     home_page.click_left_menu('Find Transactions')
#     find_transactions_page.verify_title_correct('Find Transactions')
#     find_transactions_page.find_transaction_by_category('transaction_amount', transfer_amount)
#     find_transactions_page.verify_title_correct('Transaction Results')

def test_register(page):
    register_page = RegisterPage(page)
    register_page.fill_register_info()
    register_page.verify_register_success()

def test_open_new_account(page):
    home_page = HomePage(page)
    open_account_page = OpenAccountPage(page)
    account_overview_page = AccountOverviewPage(page)
    home_page.click_left_menu('Open New Account')
    open_account_page.verify_title_correct('Open New Account')
    new_account_balance = open_account_page.get_new_account_balance()
    open_account_page.open_new_account()
    open_account_page.verify_title_correct('Account Opened!')
    new_account = open_account_page.save_new_account_number()
    home_page.click_left_menu('Accounts Overview')
    account_overview_page.verify_title_correct('Accounts Overview')
    account_overview_page.verify_account_balance(new_account, new_account_balance)

def test_transfer_fund(page):
    home_page = HomePage(page)
    transfer_funds_page = TransferFundsPage(page)

    home_page.click_left_menu('Transfer Funds')
    transfer_funds_page.verify_title_correct('Transfer Funds')

    transfer_funds_page.transfer_fund(first_account=new_account, transfer_amount=transfer_amount)
    transfer_funds_page.verify_title_correct('Transfer Complete!')

def test_bill_pay(page):
    home_page = HomePage(page)
    bill_pay_page = BillPayPage(page)

    home_page.click_left_menu('Bill Pay')
    bill_pay_page.verify_title_correct('Bill Payment Service')
    bill_pay_page.fill_bill_info()
    bill_pay_page.verify_title_correct('Bill Payment Complete')

def test_find_transactions(page):
    home_page = HomePage(page)
    find_transactions_page = FindTransactionsPage(page)

    home_page.click_left_menu('Find Transactions')
    find_transactions_page.verify_title_correct('Find Transactions')
    find_transactions_page.find_transaction_by_category('transaction_amount', transfer_amount)
    find_transactions_page.verify_title_correct('Transaction Results')

def test_force_failure():
    """Test to force a failure for demonstration purposes."""
    assert False, "This is a forced failure for testing purposes."