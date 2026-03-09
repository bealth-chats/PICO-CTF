import time
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://candy-mountain.picoctf.net:64869'))
print("Connected:", w3.is_connected())

# Let's loop more times and check
for _ in range(30):
    try:
        pending = w3.eth.get_block('pending', full_transactions=True)
        if pending.transactions:
            print("Found transactions!")
            for tx in pending.transactions:
                print(tx.hash.hex(), tx.input.hex())
            break
    except Exception as e:
        pass
    time.sleep(1)
