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
