slot2 = "7069636f4354467b6d336d7030306c5f68333173745f30333264626162317d3e"
# The last byte 3e = 62, which means the string is 31 bytes long, encoded as length * 2
print(bytes.fromhex(slot2[:-2]).decode())
