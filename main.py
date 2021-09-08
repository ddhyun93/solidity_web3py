import logging
import pprint

from web3 import Web3
from deploy_functions import utils

logging.basicConfig(format='[%(asctime)s] >> %(message)s', level=logging.INFO)


# test connection with Ganache network
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

SOURCE_CODE_PATH = "./sol/Ballot.sol"

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
deployed_contract = utils.deploy_contract(w3, contract_interface, _from, _gas_price, _gas_limit)
contract_receipt = utils.get_transaction_receipt(w3, deployed_contract)
contract_address = contract_receipt.get("contractAddress")
receipt = pprint.pformat(dict(contract_receipt))

logging.info(f"Deploy Contract  :::::: {contract_id=} deploy to block address : {contract_address}")
logging.info(f"Contract Receipt :::::: \n{receipt}")

# store_var_contract = w3.eth.contract(address=contract_address,
#                                      abi=contract_interface["abi"])

