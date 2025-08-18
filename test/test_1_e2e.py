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

def test_register(fresh_page, env_config):
    register_page = RegisterPage(fresh_page, env_config)
    register_page.click_register()
    register_page.fill_register_info()
    register_page.verify_register_success()

def test_open_new_account(page, env_config):
    home_page = HomePage(page, env_config)
    open_account_page = OpenAccountPage(page, env_config)
    account_overview_page = AccountOverviewPage(page, env_config)
    home_page.click_left_menu('Open New Account')
    open_account_page.verify_title_correct('Open New Account')
    new_account_balance = open_account_page.get_new_account_balance()
    open_account_page.open_new_account()
    open_account_page.verify_title_correct('Account Opened!')
    new_account = open_account_page.save_new_account_number()
    home_page.click_left_menu('Accounts Overview')
    account_overview_page.verify_title_correct('Accounts Overview')
    account_overview_page.verify_account_balance(new_account, new_account_balance)

def test_transfer_fund(page, env_config):
    home_page = HomePage(page, env_config)
    transfer_funds_page = TransferFundsPage(page, env_config)

    home_page.click_left_menu('Transfer Funds')
    transfer_funds_page.verify_title_correct('Transfer Funds')

    transfer_funds_page.transfer_fund(first_account=new_account, transfer_amount=transfer_amount)
    transfer_funds_page.verify_title_correct('Transfer Complete!')

def test_bill_pay(page, env_config):
    home_page = HomePage(page, env_config)
    bill_pay_page = BillPayPage(page, env_config)

    home_page.click_left_menu('Bill Pay')
    bill_pay_page.verify_title_correct('Bill Payment Service')
    bill_pay_page.fill_bill_info()
    bill_pay_page.verify_title_correct('Bill Payment Complete')

def test_find_transactions(page, env_config):
    home_page = HomePage(page, env_config)
    find_transactions_page = FindTransactionsPage(page, env_config)

    home_page.click_left_menu('Find Transactions')
    find_transactions_page.verify_title_correct('Find Transactions')
    find_transactions_page.find_transaction_by_category('transaction_amount', transfer_amount)
    find_transactions_page.verify_title_correct('Transaction Results')
