# CTF Writeup: Nested Encoding

## Challenge Description
We intercepted a suspiciously encoded message, but it’s clearly hiding a flag. No encryption, just multiple layers of obfuscation. Can you peel back the layers and reveal the truth?

## Hint
The flag has been wrapped in several layers of common encodings such as ROT13, URL encoding, Hex, and Base64. Can you figure out the order to peel them back? A tool like CyberChef can be interesting.

## Solution

The provided file `message.txt` contains the following string:
```
NjM3NjcwNjI1MDQ3NTMyNTM3NDI2MTcyNjY2NzcyNzE1ZjcyNjE3MDMwNzE3NjYxNzQ1ZjMxNzEzNzM1NmY3MjM2MzMyNTM3NDQ=
```

Based on the characters present (alphanumeric and `=` padding at the end), this is clearly Base64 encoded.

### Step 1: Base64 Decoding
Decoding the string using Base64 gives us:
```
637670625047532537426172666772715f72617030717661745f317137356f723633253744
```

### Step 2: Hex Decoding
The result from Step 1 consists entirely of hexadecimal characters (`0-9` and `a-f`). Decoding this hex string yields:
```
cvpbPGS%7Barfgrq_rap0qvat_1q75or63%7D
```

### Step 3: URL Decoding
The string from Step 2 contains `%7B` and `%7D`, which are URL encodings for `{` and `}` respectively. URL decoding the string gives:
```
cvpbPGS{arfgrq_rap0qvat_1q75or63}
```

### Step 4: ROT13 Decoding
The string format `cvpbPGS{...}` looks very similar to our expected flag format `picoCTF{...}`. The letters seem to be shifted. Applying a ROT13 cipher (which shifts letters by 13 positions) reveals the final flag:
```
picoCTF{nested_enc0ding_1d75be63}
```

## Python Script
We can write a quick Python script to automate these steps:

```python
import base64
import binascii
import urllib.parse
import codecs

with open("message.txt", "r") as f:
    msg = f.read().strip()

# Step 1: Base64 decode
msg = base64.b64decode(msg)

# Step 2: Hex decode
msg = binascii.unhexlify(msg).decode('utf-8')

# Step 3: URL decode
msg = urllib.parse.unquote(msg)

# Step 4: ROT13 decode
flag = codecs.decode(msg, 'rot_13')

print("Flag:", flag)
```

**Flag**: `picoCTF{nested_enc0ding_1d75be63}`
