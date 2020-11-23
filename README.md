# Easy voucher for UberEats and Foodora

[![Version](https://img.shields.io/github/v/release/ekvanox/easy-voucher)](https://img.shields.io/github/v/release/ekvanox/easy-voucher)
![GitHub repo size](https://img.shields.io/github/repo-size/ekvanox/easy-voucher)
[![CodeFactor](https://www.codefactor.io/repository/github/ekvanox/easy-voucher/badge)](https://www.codefactor.io/repository/github/ekvanox/easy-voucher)
![License](https://img.shields.io/github/license/ekvanox/easy-voucher)

A python script that programmatically creates and applies vouchers to accounts for UberEats and Foodora.

This script does not utilize any exploit, but will allow for users with access to multiple SIM-cards to create accounts faster.

## Installation

To clone and run this repository you'll need Git and python3 (which includes pip) installed on your computer. From your command line:

```bash
# Clone this repository
git clone https://github.com/ekvanox/easy-voucher
# Go into the repository
cd easy-voucher
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quickstart

Just run the script and follow the instructions:

```bash
# Go into the code directory
cd easy-voucher
# Execute the script
python3 main.py
```

### Advanced usage

You can configure default credentials in the `defaults.json` file located in `easy-voucher/easy-voucher`

By default the file will look like this:
```json
{
  "service": "",
  "firstName": "",
  "lastName": "",
  "emailAddress": false,
  "phoneNumber": "",
  "password": "",
  "vouchers": {
    "UberEats": ["eats-9r5j5l"],
    "Foodora": ["b70ccc007b52b6b3aa1ce48c6915497f"]
  }
}
```

To set a default value for a specific key, the value has to be set to a non empty string.

For example, a config file where all account should use the service UberEats, with the name "John Doe" and the password "Password123" would look like this:
```json
{
  "service": "UberEats",
  "firstName": "John",
  "lastName": "Doe",
  "emailAddress": false,
  "phoneNumber": "",
  "password": "Password123",
  "vouchers": {
    "UberEats": ["eats-9r5j5l"],
    "Foodora": ["b70ccc007b52b6b3aa1ce48c6915497f"]
  }
}
```

The email address key can have the value ```true```, which will result in the script using a random email address each time.


## License

This project is released under the MIT license
