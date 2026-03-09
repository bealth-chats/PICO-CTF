import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("candy-mountain.picoctf.net", 61433))

def read_until(s, prompt):
    data = b""
    while prompt not in data:
        chunk = s.recv(1024)
        if not chunk:
            break
        data += chunk
    return data

print(read_until(s, b"==> ").decode())
s.sendall(b"eee\n")
print(read_until(s, b"==> ").decode())
