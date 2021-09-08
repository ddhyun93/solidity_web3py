import logging

from web3 import Web3
from solcx import compile_source

logging.basicConfig(format='[%(asctime)s] >> %(message)s', level=logging.INFO)


# open source code
def open_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        source = f.read()
    return source


def compile_source_code(source: str) -> dict:
    return compile_source(source)


def deploy_contract(w3: Web3, contract_interface: dict, _from, _gas_price, _gas_limit):
    """
    계약을 배포합니다.
    """
    constructor = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    ).constructor(2)
    tx_hash = constructor.transact({'from': _from, 'gasPrice': _gas_price, 'gas': _gas_limit})
    logging.info(f"Estimated Gas    :::::: {constructor.estimateGas()}")
    return tx_hash


def get_transaction_receipt(w3: Web3, tx_hash) -> dict:
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    return receipt


def get_contract_address(w3: Web3, tx_hash):
    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address


def get_contract(w3: Web3, address, abi):
    registered_contract = w3.eth.contract(address=address, abi=abi)
    return registered_contract