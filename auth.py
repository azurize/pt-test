import json
import logging
import requests

from getpass import getpass

logging.basicConfig(
    level=logging.ERROR,
    format='{asctime} {levelname:<8} {message}',
    style='{'
)

# Environments
SANDBOX = 'https://sandbox.primetrust.com'
PROD = 'https://api.primetrust.com'

# Setting environment
env_choice = input(
    '\n1. Sandbox\n2. Production\nPlease choose an environment: ')

while(True):
    if env_choice == '1':
        path = f'{SANDBOX}/auth/jwts'
        break
    elif env_choice == '2':
        path = f'{PROD}/auth/jwts'
        break
    else:
        logging.error(
            'Invalid attribute. Please re-run script and enter a value of either 1 (sandbox) or 2 (production).')

# Email & password collection
EMAIL = input('\nEnter API User email: ')
PASS = getpass('\nEnter the password associated with your User: ')

otp_check = input('\nIs 2FA enabled on your API user? (Y/N): ').lower()

while(True):
    if otp_check == 'y':
        OTP = input(
            '\nPlease enter your one time password from your authentication app: ')
        break
    elif otp_check == 'n':
        print('\nThank you.')
        break
    else:
        logging.error('Invalid attribute. Please try again.')

# Expiration date confirmation
print('\nIf not included, the default expiration period of a JWT is 7 days\n')

date_check = input('Would you like to set an expiration date? (Y/N): ').lower()

if date_check == 'y':
    date = input(
        '\nIf applicable, please put an expiration date for the JWT (Format: YYYY-MM-DD): ')
elif date_check == 'n':
    date = None
    print('\nThank you.\n')
else:
    logging.error('Invalid attribute. Please try again.')

# Set the payload
if date != None and otp_check == 'y':
    payload = {
        'expires_at': date,
        'otp': OTP
    }
elif date != None and otp_check == 'n':
    payload = {
        'expires_at': date
    }
elif date == None and otp_check == 'y':
    payload = {
        'otp': OTP
    }
else:
    payload = {}

# Send POST request
r = requests.post(path, auth=(EMAIL, PASS), data=payload)

# Print results
status = str(r.status_code)

if r.ok:
    print('Success!')
    r = r.json()
    print('\nYour new token: \n\n' + r['token'])
else:
    logging.error('Error creating a JWT. Please see response below: \n')
    logging.error(json.dumps(r.json(), indent=4, sort_keys=True))
