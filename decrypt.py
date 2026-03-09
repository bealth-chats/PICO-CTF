import sys
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

sys.path.append('.')
import data

with open('coeffs.txt') as f:
    coeffs = eval(f.read())

coeffs.reverse()
c_0 = coeffs[0]
MASTER_KEY = long_to_bytes(c_0)

enc_flag_hex = data.enc_flag[1]
iv_hex = data.enc_flag[0]

enc_flag = bytes.fromhex(enc_flag_hex)
iv = bytes.fromhex(iv_hex)

cipher = AES.new(MASTER_KEY, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(enc_flag), 16)

print(pt.decode())
