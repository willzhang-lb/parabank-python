# Parabank UI & API Automation with CI/CD integrated

## Overview
This project is designed to automate end-to-end testing for a web application using Python and Playwright. It includes functionalities such as user registration, account creation, fund transfer, bill payment, and transaction search. In addition, CI/CD is integrated with github actions and Jenkins pipeline.
Three environments are set up for testing: dev, qa, and prod. (only qa url is valid)

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
$ git clone https://github.com/willzhang-lb/parabank.git
$ cd parabank
$ pip install -r requirements.txt
```

**Install playwright**
```shell
playwright install
```

**Run test**
```shell
pytest --env qa
```

**Project Structure**
```

├───.github
│   └───workflows
├───api
├───data
├───pages
├───test
├───trace
├───allure-report

