import re
import questionary
import json
import requests
import selenium

# Load vouchers into memory
with open('vouchers.json') as f:
    vouchers = json.load(f)


# Select service to create account for
service = questionary.select(
    "Select service",
    choices=[
        'Foodora',
        'UberEats',
    ]).ask()

# Enter first name to register account with
first_name = input("Enter first name:")

# Enter surname to register account with
last_name = input("Enter last name:")

# Enter email address to connect to account
email_address = input("Enter account email address:")

# Enter phone number to connect to account
phone_number = input("Enter account phone number:")

# Enter account password
password = input("Enter account password:")

# Select voucher
voucher = questionary.select(
    "Select voucher",
    choices=vouchers[service]+['None', 'Add new voucher']).ask()

if service == 'Foodora':
    # Create account
    session = requests.Session()

    # Headers
    headers = {
        'Host': 'www.foodora.se',
        'Connection': 'keep-alive',
        'Content-Length': '802',
        'Accept': 'application/json',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.108 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryFTGSOBzIezu2pajw',
        'Origin': 'https://www.foodora.se',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.foodora.se/login/new?step=registration',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Data
    data = f'''------WebKitFormBoundaryFTGSOBzIezu2pajw
Content-Disposition: form-data; name="_target_path"

/referral/result?code={voucher}
------WebKitFormBoundaryFTGSOBzIezu2pajw
Content-Disposition: form-data; name="customer[first_name]"

{first_name}
------WebKitFormBoundaryFTGSOBzIezu2pajw
Content-Disposition: form-data; name="customer[last_name]"

{last_name}
------WebKitFormBoundaryFTGSOBzIezu2pajw
Content-Disposition: form-data; name="customer[email]"

{email_address}
------WebKitFormBoundaryFTGSOBzIezu2pajw
Content-Disposition: form-data; name="customer[password]"

{password}
------WebKitFormBoundaryFTGSOBzIezu2pajw
Content-Disposition: form-data; name="customer[marketing_consent]"

opt-in
------WebKitFormBoundaryFTGSOBzIezu2pajw--'''

    r = session.post(
        url='https://www.foodora.se/api/v1/customers/async_register',
        headers=headers,
        data=data,
        verify=False,
    )

    # Enter phone number
    user_id = r.json()['user_id']

    json = {"first_name": first_name, "last_name": last_name, "email": email_address, "mobile_number": phone_number[1:], "mobile_country_code": "+46", "id": user_id, "code": "opy1fe6y", "password": "", "reference_code": "", "has_password": True,
            "sms_verification_needed": True, "sms_verification_attempts": None, "customer_addresses": [], "source": "b2c", "customer_additional_fields": [], "terms_and_conditions_consent": None, "marketing_consent": None, "customer_additional_fields_order": []}

    r = session.put(
        url=f'https://www.foodora.se/api/v1/customers/{user_id}',
        headers=headers,
        json=json,
        verify=False,
    )

    # Enter voucher
    headers = {
        "Host": "www.foodora.se",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }

    r = session.get('https://www.foodora.se/referral/result',
                    params={'code': voucher},
                    headers=headers)
