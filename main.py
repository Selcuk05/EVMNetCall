import json
import os
from getpass import getpass
from pathlib import Path

import web3
from eth_utils import is_dict, is_list_like
from web3.middleware import geth_poa_middleware

from cmd_utils import fail, inpexit, success, warn
from config import load_config


def is_view(abi, function_name):
    for index in abi:
        if index["name"] == function_name and index["stateMutability"] == "view":
            return True
    return False


os.system("color")

conf = load_config("config.py")

_ = 1
for network in conf.networks:
    print(f"{_}) {network} : {conf.networks[network]['name']}")
    _ += 1
_ = 0


network = None
while True:
    network = str(input("Choose network name: "))
    if network in conf.networks != None:
        print(success(f"Selected network: {network}"))
        break
    print(fail("Network not found in config, try again"))

w3 = web3.Web3(web3.HTTPProvider(conf.networks[network]["rpc"]))
if w3.isConnected():
    print(success(f"Connected to {network}"))
else:
    print(fail(f"Could not connect to HTTP Provider: {conf.networks[network]['rpc']}"))
    inpexit()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = None
read_only = True
path = Path("keystore.json")
if path.is_file():
    print(success("'keystore.json' found"))
    print(warn("If you want read-only mode, you can leave the following input empty."))
    print(warn("Your keystore should be named 'keystore.json'."))
    passwd = getpass("Enter keystore password: ")
    if not passwd.strip() == "":
        path = Path("keystore.json")
        if path.is_file():
            with open("keystore.json") as f:
                data = json.load(f)
                account = w3.eth.account.privateKeyToAccount(
                    w3.eth.account.decrypt(data, passwd)
                )
                print("Account imported:", success(account.address))
                w3.eth.default_account = account.address
                read_only = False
                print("Read-Only:", fail("OFF"))
    else:
        print("Read-Only:", success("ON"))
else:
    print(warn("'keystore.json' not found"))
    print("Read-Only:", success("ON"))

addr = None
while True:
    addr = str(input("Contract address: "))
    if w3.isChecksumAddress(addr):
        print(success("Checksum Address: OK"))
        break
    print(fail("Not checksum address, try again"))

abi = None
while True:
    abi_file_name = str(input("ABI file name (JSON): "))
    path = Path(abi_file_name)
    if path.is_file() and (os.path.splitext(abi_file_name)[1] == ".json"):
        with open(abi_file_name) as f:
            abi = json.load(f)
        if is_list_like(abi) and all([is_dict(i) for i in abi]):
            print(success("ABI: Valid"))
            break
        print(fail("The ABI is not valid structure wise. Change it and try again"))
    print(fail("File not found or not JSON, try again"))

contract = w3.eth.contract(address=addr, abi=abi)
print("\nContract Functions")
_ = 1

for func in contract.all_functions():
    print(f"{success(str(_) + ')')} {func}")
    _ += 1

while True:
    used_func = str(input("Enter desired function name (type exit to exit): "))

    if used_func == "exit":
        inpexit()

    if not used_func in contract.functions:
        print(fail("Enter a valid contract name."))
        continue
    func_to_call = contract.functions[used_func]

    print("\n" + warn("Enter parameters divided with commas"))
    print(warn("add 'is_number' at the start of the parameter if it is uint256"))
    print(
        warn(
            "Example function(16: uint256, bla_bla_bla: string) => is_number16,bla_bla_bla"
        )
    )
    print(warn("Leave empty if function has no parameters."))
    params = str(input("=> "))
    params_list = []
    for param in params.split(","):
        clean_param = param.strip()
        if clean_param != "":
            if clean_param.startswith("is_number"):
                clean_param = int(clean_param.replace("is_number", ""))
            params_list.append(clean_param)

    if is_view(abi, used_func):
        result = func_to_call(*params_list).call()
        print("Result: " + success(str(result)) + "\n")
        continue

    if read_only == False:
        nonce = w3.eth.get_transaction_count(account.address)
        txn = func_to_call(*params_list).buildTransaction(
            {
                "nonce": nonce,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(
            txn, private_key=account.privateKey
        )
        try:
            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print("Transaction hash:", txn_hash.hex())
        except Exception as e:
            print(fail("Error: " + e))
            continue
    else:
        print(warn("Function not available in read-only mode as it changes state"))
    continue
