# End-to-End Testing Project

## Overview
This project is designed to automate end-to-end testing for a web application using Python and Playwright. It includes functionalities such as user registration, account creation, fund transfer, bill payment, and transaction search.

## Structure
pages 
   ├── base_page.py
   ├── home_page.py 
test 
   ├── test_e2e.py 
├── utils 
├── requirements.txt 
├── member_info.json 
├── conftest.py 
└── README.md
   
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

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Running Tests
   Run the end-to-end tests:
      ```bash
      pytest test/test_e2e.py


