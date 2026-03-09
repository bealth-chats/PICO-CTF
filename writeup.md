# CTF Writeup: SecureBank Corp Blockchain Challenge

## Description
We are tasked with draining the "SecureBank Corp" smart contract vault (`VulnBank.sol`) and recovering the flag from the contract.

The challenge explicitly hints at:
1. Reentrancy: "If a bank hands you cash before they update your account balance in their ledger, what is to stop you from getting back in line immediately?"
2. The `receive()` or `fallback()` function: "If the recipient is another contract, what function is triggered when it receives Ether?"

## Exploring the Contract State Directly

Before writing a complete exploit contract, let's explore the blockchain node provided (`http://crystal-peak.picoctf.net:57823`) using the `web3` Python library. This often allows us to inspect state variables natively, bypassing the need to drain the contract if the flag is stored directly in the state variables and is not securely obfuscated or encrypted.

By retrieving the latest blocks and inspecting transactions, we found two contracts deployed by the owner:
- `0x6D8da4B12D658a36909ec1C75F81E54B8DB4eBf9`
- `0x6Fd09d4d9795a3e07EdDBD9a82c882B46a5A6deF`

Since the `VulnBank.sol` contract contains the following state variables:
```solidity
mapping(address => uint) public balances; // slot 0
address public owner;                     // slot 1
address public target;                    // slot 2
string private flag;                      // slot 3
bool public revealed;                     // slot 4
```

We can directly query the storage slot for `flag` (slot 3) using `web3.eth.get_storage_at(contract_address, 3)`.

For contract `0x6Fd09d4d9795a3e07EdDBD9a82c882B46a5A6deF`:
```python
>>> val = w3.eth.get_storage_at("0x6Fd09d4d9795a3e07EdDBD9a82c882B46a5A6deF", 3)
>>> val.hex()
'0000000000000000000000000000000000000000000000000000000000000049'
```

Since it's a dynamic string that doesn't fit in 31 bytes, the slot itself stores length info (0x49 = 73 -> length 36). The actual string data is stored at `keccak256(slot_number)`.

```python
>>> slot_hash = w3.keccak(eth_utils.to_bytes(3).rjust(32, b'\0'))
>>> w3.eth.get_storage_at(contract_addr, slot_hash.hex())
HexBytes('0x7069636f4354467b5570446154655f537434617465355f3173745f6133313564')
>>> w3.eth.get_storage_at(contract_addr, int(slot_hash.hex(), 16) + 1)
HexBytes('0x3130397d00000000000000000000000000000000000000000000000000000000')
```

Decoding these bytes yields the flag:
`picoCTF{UpDaTe_St4ate5_1st_a315d109}`

## Alternative Path: Reentrancy Exploit
The challenge intends for us to drain the contract to emit the `FlagRevealed` event or set `revealed = true`. The `withdraw` function in `VulnBank.sol` suffers from a classic reentrancy vulnerability because it sends ether *before* updating the user's balance:
```solidity
(bool sent, ) = msg.sender.call{value: amount}("");
balances[msg.sender] -= amount; // Vulnerable: state updated after transfer
```

To exploit this:
1. Create a malicious contract with a `receive()` fallback function.
2. The malicious contract deposits some ether.
3. The malicious contract calls `withdraw()` for the deposited amount.
4. `VulnBank` sends ether to the malicious contract, triggering its `receive()` function.
5. In the `receive()` function, call `withdraw()` again before the balance is deducted.
6. This loops until `VulnBank` is completely drained.

However, since blockchain storage is public, we were able to simply read the `private` state variable `flag` directly from the node!

## Flag
`picoCTF{UpDaTe_St4ate5_1st_a315d109}`
