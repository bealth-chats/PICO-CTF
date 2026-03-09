with open("system.out", "rb") as f:
    data = f.read()

# search for 'picoCTF{' XORed with any single byte
target = b"picoCTF{"
for i in range(len(data) - len(target)):
    key = data[i] ^ target[0]
    match = True
    for j in range(1, len(target)):
        if data[i+j] ^ key != target[j]:
            match = False
            break
    if match:
        print(f"Found flag at offset {i} with key {key}")
        flag = ""
        for j in range(100):
            c = data[i+j] ^ key
            if c == 0 or c > 127:
                break
            flag += chr(c)
        print("Flag:", flag)
