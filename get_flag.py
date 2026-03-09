import sys

def hash_str(s):
    h = 0x1505
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xffffffffffffffff
    return h

secret = "iUbh81!j*hn!"
print("picoCTF{" + str(hash_str(secret)) + "}")
print("picoCTF{" + secret + "}")
