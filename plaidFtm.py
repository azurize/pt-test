import json
import logging
import os
import requests

from dotenv import load_dotenv

load_dotenv('.env')

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} {levelname:<8} {message}',
    style='{'
)

PT_ENV = 'https://sandbox.primetrust.com'
PLAID_ENV = 'https://sandbox.plaid.com'

HEADERS = {'Authorization': 'Bearer ' + os.environ.get('TOKEN')}

# Plaid Quickstart : https://plaid.com/docs/quickstart/ -- THIS FLOW MUST BE COMPLETED PRIOR TO RUNNING THIS SCRIPT

# When testing quickstart widget:
# username = user_good
# password = pass_good

confirmation = input(
    'Have you completed the Plaid Quickstart workflow (Y/N)?: ').lower()

if confirmation != 'y':
    logging.warning(
        'Please complete the quickstart workflow at: https://plaid.com/docs/quickstart/ and then re-run this script.')
else:
    accessToken = input('ENTER ACCESS TOKEN: ')

    # Retrieve Plaid account id via Plaid access token

    logging.info('Retrieving Plaid account...')

    path = f'{PLAID_ENV}/accounts/get'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        'client_id': os.environ.get('CLIENT_ID'),
        'secret': os.environ.get('SECRET'),
        'access_token': accessToken
    })
    r = requests.post(path, headers=headers, data=payload).json()
    account_id = r['accounts'][0]['account_id']
    logging.info('Plaid Account ID: ' + account_id)

    # Create processor token with Plaid account ID and Plaid access token

    logging.info('Creating Plaid processor token...')

    path = f'{PLAID_ENV}/processor/token/create'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        'client_id': os.environ.get('CLIENT_ID'),
        'account_id': account_id,
        'secret': os.environ.get('SECRET'),
        'access_token': accessToken,
        'processor': 'prime_trust'
    })
    r = requests.post(path, headers=headers, data=payload).json()
    logging.info(json.dumps(r, indent=2, sort_keys=True))
    processorToken = r['processor_token']

    # Create funds transfer method with Plaid processor token

    path = f'{PT_ENV}/v2/funds-transfer-methods'
    payload = json.dumps({
        "data": {
            "type": "funds-transfer-method",
            "attributes": {
                "funds-transfer-type": "ach",
                "ach-check-type": "personal",
                "contact-id": os.environ.get('CONTACT_ID'),
                "plaid-processor-token": processorToken
            }
        }
    })
    r = requests.post(path, headers=HEADERS, data=payload).json()
    logging.info('Funds transfer method created with an ID of: ' + r['data']['id'])