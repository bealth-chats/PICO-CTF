from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://candy-mountain.picoctf.net:64869'))

tx = w3.eth.get_transaction('0xf8ee30502eb373fd7e4d2beefd1902262717156b949bde3533a863f0f896e1f7')
print(tx)
print("To:", tx.to)
