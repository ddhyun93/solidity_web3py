from web3 import Web3
from solcx import compile_source


# open source code
def open_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        source = f.read()
    return source


def compile_source_code(source: str) -> dict:
    return compile_source(source)


def deploy_contract(w3: Web3, contract_interface: dict, _from, _gas_price, _gas_limit):
    """
    계약을 배포하고 계약이(tx) 기록된 블록의 주소를 반환합니다.
    """
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    ).constructor(2).transact({'from': _from, 'gasPrice': _gas_price, 'gas': _gas_limit})
    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address
