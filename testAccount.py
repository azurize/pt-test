import json
import logging
import os
import random
import requests

from dotenv import load_dotenv

load_dotenv('.env')

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} {levelname:<8} {message}',
    style='{'
)

ENV = 'https://sandbox.primetrust.com'
HEADERS = {'Authorization': 'Bearer ' + os.environ.get('TOKEN')}

# Create a random test custodial account
logging.info('Creating test custodial account...')

path = f'{ENV}/v2/accounts?include=contacts'
payload = json.dumps({
    "data": {
        "type": "account",
        "attributes": {
            "account-type": "custodial",
            "name": "Test Account " + str(random.randint(1, 100000)),
            "authorized-signature": "Test Person",
            "owner": {
                "contact-type": "natural_person",
                "name": "John Jones",
                "email": "john@example.com",
                "date-of-birth": "1990-01-01",
                "tax-id-number": "867530986",
                "tax-country": "US",
                "primary-phone-number": {
                    "country": "US",
                    "number": "5558675309",
                    "sms": False
                },
                "primary-address": {
                    "street-1": "123 Test Ave",
                    "street-2": "",
                    "postal-code": "90210",
                    "city": "Los Angeles",
                    "region": "CA",
                    "country": "US"
                }
            }
        }
    }
})
r = requests.post(path, headers=HEADERS, data=payload).json()

account_id = r["data"]["id"]
contact_id = r["data"]["relationships"]["contacts"]["data"][0]["id"]

logging.info('Done.')

# Upload KYC Documents
logging.info("Uploading test KYC documents...")

path = f'{ENV}/v2/uploaded-documents'
payload = {'contact-id': contact_id,
    'label': 'Passport',
    'public': 'true',
    'extension' : 'jpg'
    }
files = [
    ('file', ('file', open('static/images/passport.jpg', 'rb'), 'application/octet-stream'))
]
r = requests.post(path, headers=HEADERS, data=payload, files=files)

if r.ok:
    logging.info('Done.')
    r = r.json()
    doc_id = r['data']['id']
else:
    logging.error('There was an error submitting the test document.')
    logging.error(json.dumps(r.json(), indent=4, sort_keys=True))
    exit(0)

logging.info('Running test KYC document check...')

path = f'{ENV}/v2/kyc-document-checks'
payload = json.dumps({
    "data": {
        "type": "kyc-document-checks",
        "attributes": {
            "contact-id": contact_id,
            "uploaded-document-id": doc_id,
            "kyc-document-type": "passport",
            "identity": True,
            "identity-photo": True,
            "proof-of-address": False,
            "kyc-document-country": "US"
        }
    }
})
r = requests.post(path, headers=HEADERS, data=payload)

if r.ok:
    r = r.json()
    doc_check_id = r['data']['id']
    logging.info('Done.')
else:
    logging.error('Error submitting KYC document check.')
    logging.error(json.dumps(r.json(), indent=4, sort_keys=True))
    exit(0)

# Approve KYC document check
logging.info('Verifying KYC document check...')

path = f'{ENV}/v2/kyc-document-checks/{doc_check_id}/sandbox/verify'
r = requests.post(path, headers=HEADERS)

if r.ok:
    logging.info('Done.')
else:
    logging.error('Error verifying KYC document check.')
    logging.error(json.dumps(r.json(), indent=4, sort_keys=True))
    exit(0)

logging.info('ACCOUNT ID: ' + account_id)
logging.info('CONTACT ID: ' + contact_id)
