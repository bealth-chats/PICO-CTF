# Blockchain CTF Writeup

## Challenge Description
A mysterious vault has been discovered on the blockchain. It's programmed to release a secret flag to anyone who can provide the correct pre-image to a specific hash.
Our sensors indicate that a "Victim Bot" has found the answer and is currently trying to submit it, but they are being very stingy with their gas price.
Additional details will be available after launching your challenge instance.

## Solution

The hint given mentions looking at the pending transactions in the mempool.
The node provided is at `candy-mountain.picoctf.net:64869`.
The `FrontRunning.sol` contract reveals there is a `solve(string memory solution)` function, which accepts the correct pre-image that hashes to a target hash.

Since the Victim Bot is trying to submit the solution but with a stingy gas price, the transaction sits in the mempool waiting to be mined.

We can inspect the pending block using Python and the `web3` library:

```python
import time
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://candy-mountain.picoctf.net:64869'))
print("Connected:", w3.is_connected())

for _ in range(30):
    try:
        pending = w3.eth.get_block('pending', full_transactions=True)
        if pending.transactions:
            print("Found transactions!")
            for tx in pending.transactions:
                print("TX Hash:", tx.hash.hex())
                print("TX Input Data:", tx.input.hex())
            break
    except Exception as e:
        pass
    time.sleep(1)
```

Running this code successfully captured a pending transaction:

```
Found transactions!
TX Hash: f8ee30502eb373fd7e4d2beefd1902262717156b949bde3533a863f0f896e1f7
TX Input Data: 76fe1e92000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000177069636f4354467b6d336d7030306c5f7031723474337d000000000000000000
```

The input data represents the ABI-encoded call to `solve(string memory solution)`:
- `76fe1e92`: Function selector.
- `0000000000000000000000000000000000000000000000000000000000000020`: Offset to the string data.
- `0000000000000000000000000000000000000000000000000000000000000017`: The length of the string, which is `0x17` (23 bytes).
- `7069636f4354467b6d336d7030306c5f7031723474337d000000000000000000`: The encoded string padded to 32 bytes.

Converting the hex string `7069636f4354467b6d336d7030306c5f7031723474337d` back to ASCII gives:

```
picoCTF{m3mp00l_p1r4t3}
```

## Flag
`picoCTF{m3mp00l_p1r4t3}`
