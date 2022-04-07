----------
| README |
----------

Updated: 4/7/2022

Pre-requisites: 
- Python 3.10+ must be installed
- If using a virtual environment, make sure it is enabled prior to installing required modules

Instructions

1. Install any required modules via 'pip install -r requirements.txt'
2. Enter your JWT and any of the applicable variables in a .env file (.env.example is included)
    2a. You can create a new JWT with auth.py
3. Open a terminal and run script of your choice

Instructions for using widgets

1. Ensure that you have installed the requirements specified in requirements.txt
2. Open a terminal, navigate to the directory holding "app.py" and run the following command: flask run
3. Navigate to whichever route you are trying to access as specified in "app.py" (e.g. 127.0.0.1/addcard/)

Index:
<!-- Authentication -->
-- auth.py : Creates a JWT  

<!-- Accounts/Compliance -->
-- testAccount.py : Creates a randomly generated test custodial account (using happy path PII) with all checks created/passed

<!-- Flask -->
-- app.py : Application configuration to define all routes and functions for each action

<!-- Payment Rails -->
-- plaidFtm.py : Creates a Plaid-linked funds transfer method (must have Plaid access token available before using)

<!-- Misc. -->
-- issuance.py : Creates a cardholder and verifying the card holder in debit card issuance flow
    * Requires enablement on the Prime Trust side in order to function properly, and values to be prefilled for the account and contact ID