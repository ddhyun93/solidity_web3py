import os, sys
import logging
import pprint

from web3 import Web3
from deploy_functions import utils

logging.basicConfig(format='[%(asctime)s] >> %(message)s', level=logging.INFO)


# test connection with Ganache network
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

SOURCE_CODE_PATH = "../sol/Ballot.sol"        # using when deploy
# SOURCE_CODE_PATH = "./sol/Ballot.sol"        # using when interact with API

'''
details about gas ; refer https://steemit.com/kr/@jinkim/gas-gas-limit-block-gas-limit-gas-price-total-fee
'''
# accounts that deploy this contract
_from = w3.eth.accounts[0]
# the amount of Gwei that the user is willing to spend on each unit of Gas.
_gas_price = w3.eth.gasPrice
# maximum amount of Gas that a user willing to pay for blcok 편입 (블록에 내 트랜잭션이 기록될 때 지불할 용의가 있는 최대 가스량)
_gas_limit = w3.eth.getBlock('latest').gasLimit

# compile solidity source code
COMPILED_SOL = utils.compile_source_code(utils.open_file(SOURCE_CODE_PATH))

# deploy contract
contract_id, contract_interface = COMPILED_SOL.popitem()
w3.eth.defaultAccount = w3.eth.accounts[0]
deployed_contract = w3.eth.contract(
    abi=contract_interface['abi'],
    bytecode=f"0x{contract_interface['bin']}",
    bytecode_runtime=contract_interface['bin-runtime']
    ).constructor(3)
tx_hash = deployed_contract.transact({'from': _from, 'gasPrice': _gas_price, 'gas': _gas_limit})
# tx_hash = deployed_contract.transact()
logging.info(f"Estimated Gas    :::::: {deployed_contract.estimateGas()}")
contract_receipt = w3.eth.get_transaction_receipt(tx_hash)
contract_address = contract_receipt.get("contractAddress")
receipt = pprint.pformat(dict(contract_receipt))
logging.info(f"Deploy Contract  :::::: {contract_id=} deploy to block address : {contract_address}")
logging.info(f"Contract Receipt :::::: \n{receipt}")

# smart contract object to be called and interacted with
registered_contract = w3.eth.contract(address=contract_address,
                                      abi=contract_interface['abi'])

# print(registered_contract.all_functions())
# # registered_contract.functions.changeState(1).transact()
# print(registered_contract.functions.state().call())
# registered_contract.functions.register(w3.eth.accounts[1]).transact({'from': w3.eth.accounts[0]})

# registered_contract.functions.changeState(2).transact()
print(w3.eth.get_accounts())
registered_contract.functions.register("0x859Bb37b0E2D575FF4AD6A47688edaC6431fC27F").transact({'from': "0x0A0581abd120FaceB3CAB6B9dfDb14f93Ec6340B"})

# state = "state"
# state_func = registered_contract.functions[state]
# print(state_func().call())
#
# func_to_call = "changeState"
# contract_func = registered_contract.functions[func_to_call]
# contract_func(2).call()
#
# state2 = "state"
# state_func2 = registered_contract.functions[state]
# print(state_func2().call())


# func_to_call = "register"
# contract_func = registered_contract.functions[func_to_call]
# contract_func("0x7A0F1Ce6c65Ba1468CFf871A4A1f308Bf99FE423").call()
