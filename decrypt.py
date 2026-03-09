import base64

data = "R1xbW3pndkhFBV9BCmxTAFtZZ0AJRANBaAIBBloEAQUASA=="
decoded = base64.b64decode(data)

key = b"75849303"

flag = ""
for i in range(len(decoded)):
    flag += chr(decoded[i] ^ key[i % len(key)])
print(flag)
