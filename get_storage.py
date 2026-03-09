from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://candy-mountain.picoctf.net:64869'))

contract_addr = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
for i in range(5):
    val = w3.eth.get_storage_at(contract_addr, i)
    print(f"Slot {i}: {val.hex()}")
