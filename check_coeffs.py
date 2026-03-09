import hashlib
from Crypto.Util.number import long_to_bytes

with open('coeffs.txt') as f:
    coeffs = eval(f.read())

coeffs.reverse() # Now index 0 is c_0

c_0 = coeffs[0]
c_1 = coeffs[1]

print("c_0:", hex(c_0))
print("c_1 from LLL:", hex(c_1))
expected_c_1 = hashlib.sha256(long_to_bytes(c_0)).digest().hex()
print("c_1 expected:", expected_c_1)

expected_c_2 = hashlib.sha256(long_to_bytes(c_1)).digest().hex()
print("c_2 expected:", expected_c_2)
print("c_2 from LLL:", hex(coeffs[2]))
