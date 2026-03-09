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
                with open("writeup.md", "w") as f:
                    f.write("# Reverse Engineering CTF Writeup\n\n")
                    f.write("Flag found:\n\n```\n")
                    f.write(text)
                    f.write("\n```\n")
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
