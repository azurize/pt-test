import json
import logging
import os
import requests
import time

from dotenv import load_dotenv

load_dotenv('.env')

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} {levelname:<8} {message}',
    style='{'
)

ENV = 'https://sandbox.primetrust.com'
HEADERS = {'Authorization': 'Bearer ' + os.environ.get('TOKEN')}

# You can use testAccount.py to create a random custodial account/contact for the values below

# Populate with your own account ID
ACCOUNT_ID = ''

# Populate with your own contact ID (usually associated with account)
CONTACT_ID = ''

email = input('Enter your email address (must have access to it): ')
phone = input('Enter your phone number (must have access to it): ')

logging.info('Creating card holder. Please wait...')

# Create Cardholder
path = f'{ENV}/v2/card-holders'
payload = json.dumps({
    'data': {
        'type': 'card-holders',
        'attributes': {
                'account-id': ACCOUNT_ID,
                'contact-id': CONTACT_ID,
                'email': email,
                'phone-number': phone
        }
    }
})
r = requests.post(path, headers=HEADERS, data=payload)

if r.ok:
    logging.info('Done.')
else:
    logging.error('Trouble creating the card holder.')
    error = r['errors'][0]['detail']
    logging.error('ERROR: ' + error)

logging.info(json.dumps(r.json(), indent=4, sort_keys=True))
cardHolderVer = r['data']['relationships']['card-holder-verification']['links']['related']

if r.ok:
    logging.info('Done.')
else:
    logging.error('Trouble creating the card holder.')

# Email verification
logging.info('Please wait while email verification is sent out...')

path = f'{cardHolderVer}/request-email-verification'
r = requests.post(path, headers=HEADERS)

if r.ok:
    logging.info('Email sent.')
    time.sleep(2.0)
else:
    logging.error('Error generating email')

otp = input('Please enter the one time password you were emailed: ')

logging.info('Verifying...')

path = f'{cardHolderVer}/verify-email'
payload = json.dumps({
    'data': {
        'type': 'card-holder-verifications',
        'attributes': {
            'email-otp': otp
        }
    }
})
r = requests.post(path, headers=HEADERS, data=payload).json()

if r.ok:
    logging.info('Done.')
else:
    logging.error('Unable to verify email.')