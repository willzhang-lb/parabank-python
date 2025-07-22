# Parabank UI & API Automation with CI/CD integrated

## Overview
This project is designed to automate end-to-end testing for a web application using Python and Playwright. It includes functionalities such as user registration, account creation, fund transfer, bill payment, and transaction search. In addition, CI/CD is integrated with github actions and Jenkins pipeline

## Features
UI Automation
- **User Registration**: Automates the registration process and verifies success.
- **Account Management**: Opens new accounts and verifies account details.
- **Fund Transfer**: Transfers funds between accounts and validates the transaction.
- **Bill Payment**: Automates bill payment and ensures payment completion.
- **Transaction Search**: Searches for transactions based on various criteria.

API automation
- **Transaction Search by amount**: Searches for transactions based on transfer amount.
  
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
pytest
```

**Project Structure**
```

├───member_storage.json
├───member_info.json
├───account_info.json
├───bill_info.json
├───README.md
├───conftest.py
├───utils.py
├───.env
├───requirements.txt            #dependencies
├───api                         #api object directory
├───pages                       #page object directory
├───test                        #test case directory
