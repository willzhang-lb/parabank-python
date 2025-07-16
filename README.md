# End-to-End Testing Project

## Overview
This project is designed to automate end-to-end testing for a web application using Python and Playwright. It includes functionalities such as user registration, account creation, fund transfer, bill payment, and transaction search.

## Features
- **User Registration**: Automates the registration process and verifies success.
- **Account Management**: Opens new accounts and verifies account details.
- **Fund Transfer**: Transfers funds between accounts and validates the transaction.
- **Bill Payment**: Automates bill payment and ensures payment completion.
- **Transaction Search**: Searches for transactions based on various criteria.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Playwright
- **Dependency Management**: pip


**Set up local project**
```shell
$ git clone https://github.com/lifebyte-systems/CRM-UI-Automation.git
$ cd parabank
$ pip install -r requirements.txt
```

**Create virtual environment**
```shell
python -m venv venv
```

**Install playwright**
```shell
playwright install
```

**Run test**
```shell
pytest test/
```

