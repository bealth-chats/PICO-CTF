# Reverse Engineering CTF Writeup

## Challenge Description
You think you can reverse engineer? Let's test out your speed Connect to the service! Here's the command: `nc mysterious-sea.picoctf.net 53621`

## Analysis
Connecting to the service interactively shows that the server sends a large hex string and prompts for a secret. The hex string is actually a serialized ELF 64-bit LSB executable.

If we manually download the hex string, decode it into a binary using `xxd -r -p`, and disassemble it using `objdump`, we can look for the entry point or `main` function.

Disassembly of `<main>`:
```asm
0000000000401136 <main>:
  401136:	55                   	push   %rbp
  401137:	48 89 e5             	mov    %rsp,%rbp
  40113a:	48 83 ec 10          	sub    $0x10,%rsp
  40113e:	c7 45 fc ad 68 68 71 	movl   $0x716868ad,-0x4(%rbp)
  401145:	c7 45 f8 00 00 00 00 	movl   $0x0,-0x8(%rbp)
  40114c:	bf 10 20 40 00       	mov    $0x402010,%edi
  401151:	e8 da fe ff ff       	call   401030 <puts@plt>
  401156:	48 8d 45 f8          	lea    -0x8(%rbp),%rax
  40115a:	48 89 c6             	mov    %rax,%rsi
  ...
  40116c:	8b 45 f8             	mov    -0x8(%rbp),%eax
  40116f:	39 45 fc             	cmp    %eax,-0x4(%rbp)
```
Notice that the binary initializes a stack variable with an immediate constant value (`0x716868ad`), prompts the user, reads an integer, and compares the integer read against this stack variable.

Since the service requires us to reverse engineer many of these binaries very quickly, we must automate this process.

## Automation Script
We can use a Python socket script to read the hex streams, unhexlify them to a file on disk, run `objdump`, and extract the immediate value loaded into `-0x4(%rbp)` in the `main` function.

```python
import socket
import re
import binascii
import subprocess
import os

def solve():
    host = 'mysterious-sea.picoctf.net'
    port = 53621

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(15)
        print("Connecting...")
        s.connect((host, port))

        round_num = 1
        while True:
            data = b""
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if b"secret?:" in data or b"picoCTF{" in data:
                        break
                except socket.timeout:
                    print("Timeout receiving data")
                    break

            if not data:
                print("Disconnected")
                break

            text = data.decode('utf-8', errors='ignore')
            print(f"--- Round {round_num} ---")

            if "picoCTF{" in text:
                print("FLAG FOUND!!!")
                print(text)
                break

            # Find hex data
            hex_match = re.search(r'([0-9a-fA-F]{100,})', text)
            if not hex_match:
                print("No hex found in data:", text[:200])
                break

            hex_data = hex_match.group(1)
            with open("binary", "wb") as f:
                f.write(binascii.unhexlify(hex_data))
            os.chmod("binary", 0o755)

            # Extract the secret using objdump
            result = subprocess.run(["objdump", "-d", "binary"], capture_output=True, text=True)

            # Extract <main> function
            main_match = re.search(r'<main>:(.*?)(?:^0000000000|Disassembly of section)', result.stdout, re.DOTALL | re.MULTILINE)
            if not main_match:
                print("Could not find <main> function")
                break

            main_code = main_match.group(1)

            # Find all movl instructions that move an immediate value to the stack
            mov_matches = re.findall(r'movl?\s+\$0x([0-9a-f]+),\s*-0x[0-9a-f]+\(%rbp\)', main_code)

            secret = None
            for m in mov_matches:
                val = int(m, 16)
                if val != 0:
                    secret = str(val)
                    break

            if secret:
                print(f"Extracted secret: {secret}")
                s.sendall((secret + "\n").encode())
            else:
                print("Could not find secret in main_code!")
                print(main_code)
                break

            round_num += 1

if __name__ == "__main__":
    solve()
```

## Running the Script
Running the script outputs the extracted secrets continuously until it gets the flag.
```
Connecting...
--- Round 1 ---
Extracted secret: 3814771671
--- Round 2 ---
Extracted secret: 2779422718
--- Round 3 ---
Extracted secret: 3210394317
...
--- Round 21 ---
FLAG FOUND!!!
Correct!
Woah, how'd you do that??
Here's your flag: picoCTF{4u7o_r3v_g0_brrr_78c345aa}
```

Flag: `picoCTF{4u7o_r3v_g0_brrr_78c345aa}`
