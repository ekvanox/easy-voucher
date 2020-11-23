import re
import questionary
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str


# Load vouchers into memory
with open('defaults.json') as f:
    defaults_dict = json.load(f)

# Select service to create account for
service = defaults_dict['service'] or questionary.select(
    "Select service",
    choices=[
        'Foodora',
        'UberEats',
    ]).ask()

# Enter first name to register account with
first_name = defaults_dict['firstName'] or input("Enter first name:")

# Enter surname to register account with
last_name = defaults_dict['lastName'] or input("Enter last name:")

# Enter email address to connect to account
email_address = defaults_dict['emailAddress'] or input(
    "Enter account email address:")
if email_address is True:
    email_address = f'{get_random_string(10)}@gmail.com'

# Enter phone number to connect to account
phone_number = defaults_dict['phoneNumber'] or input(
    "Enter account phone number (local):")
# Enter account password
password = defaults_dict['password'] or input("Enter account password:")

# Select voucher
voucher = questionary.select(
    "Select voucher",
    choices=defaults_dict["vouchers"][service]).ask()

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

elif service == 'UberEats':

    # Start chrome driver (requires selenium to be configured correctly beforehand)
    driver = webdriver.Chrome()

    # Load account creation page
    driver.get("https://auth.uber.com/login/?uber_client_name=eatsWebSignUp&source=auth&next_url=https%3A%2F%2Fwww.ubereats.com%2Flogin-redirect%2F%3F")

    # Select mobile number input box
    mobile_input = driver.find_element_by_id("mobile")

    # Enter phone number
    mobile_input.send_keys(phone_number[1:])
    mobile_input.send_keys(Keys.RETURN)

    time.sleep(2)

    # Select and click the google chapcha box
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3)
    actions.send_keys(Keys.SPACE)
    actions.perform()

    # Wait until user completes chapcha and OTP check, and enter email
    element = WebDriverWait(driver, 9999999).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input = driver.find_element_by_id("email")
    email_input.send_keys(email_address)
    email_input.send_keys(Keys.RETURN)
    time.sleep(1)

    # Enter first and last name
    first_name_input = driver.find_element_by_id("firstName")
    first_name_input.send_keys(first_name)
    last_name_input = driver.find_element_by_id("lastName")
    last_name_input.send_keys(last_name)
    last_name_input.send_keys(Keys.RETURN)
    time.sleep(1)

    # Enter password for account
    password_input = driver.find_element_by_id("addPassword")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(1)

    # Go to voucher entering link
    driver.get("https://www.ubereats.com/se?mod=applyPromo&ps=1")
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 2)
    actions.send_keys(voucher)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(1)

    time.sleep(10)
