import json
import logging
import os
import requests

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} {levelname:<8} {message}',
    style='{'
)

load_dotenv('.env')

ENV = 'https://sandbox.primetrust.com'
HEADERS = {'Authorization': 'Bearer ' + os.environ.get('TOKEN')}


def individualToken():
    path = f'{ENV}/v2/resource-tokens'
    payload = json.dumps({
        "data": {
            "type": "resource-tokens",
            "attributes": {
                "resource-type": "user",
                "resource-id": os.environ.get('USER_ID'),
                "resource-token-type": "create_account",
                "data": {
                    "account_types": ["custodial"],
                    "contact_types": ["natural_person"]
                }
            }
        }
    })
    r = requests.post(path, headers=HEADERS, data=payload).json()
    token = r['data']['attributes']['token']
    return token


def companyToken():
    path = f'{ENV}/v2/resource-tokens'
    payload = json.dumps({
        "data": {
            "type": "resource-tokens",
            "attributes": {
                "resource-type": "user",
                "resource-id": os.environ.get('USER_ID'),
                "resource-token-type": "create_account",
                "data": {
                    "account_types": ["custodial"],
                    "contact_types": ["company"]
                }
            }
        }
    })
    r = requests.post(path, headers=HEADERS, data=payload).json()
    token = r['data']['attributes']['token']
    return token


def linkToken():
    path = f'{ENV}/v2/credit-card-resources'
    payload = json.dumps({
        "data": {
            "type": "credit-card-resource",
            "attributes": {
                    "contact-id": os.environ.get('CONTACT_ID')
            }
        }
    })
    r = requests.post(path, headers=HEADERS, data=payload).json()
    token = r['data']['attributes']['token']
    return token

