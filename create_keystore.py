import json
import os
from getpass import getpass

import web3

from cmd_utils import fail, success, warn

os.system("color")

print(success("Ethereum Keystore Creator"))
print(warn("Your private key is needed for the decryption."))
print(warn("This program only serves to encrypt your private key."))
print(
    warn("Never give your private key to software which you can not verify the source.")
)
pk = getpass("Enter your private key: ")
passwd = None
while True:
    passwd = getpass("Enter your desired password for encryption: ")
    passwd_ver = getpass("Enter password again for verification: ")
    if passwd == passwd_ver:
        print(success("Passwords matched"))
        break
    print(fail("Passwords do not match, try again"))

w3 = web3.Web3(web3.HTTPProvider("https://mainnet.infura.io/v3/"))
v3 = w3.eth.account.encrypt(pk, passwd)

with open("keystore.json", "w") as f:
    json.dump(v3, f)
