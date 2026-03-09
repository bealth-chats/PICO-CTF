from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://candy-mountain.picoctf.net:64869'))

candidate_flag = "picoCTF{m3mp00l_p1r4t3}"

encoded = candidate_flag.encode()
hash_val = w3.keccak(encoded)
print("Hash of string directly:", hash_val.hex())
print("Expected hash: 0xd781033f8619ec5d3ab5387d3ad9b87203acce775bc100b32bfbac009e596cd6")
