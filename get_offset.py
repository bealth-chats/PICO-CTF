import sys
import struct

with open("beacon", "rb") as f:
    data = f.read()

# Let's search for some byte sequence to figure out sub_2d90
# It says "emulate sub_2d90" and "brute-force the 16-bit seed"
# Let's look for the hook 0x401c10 (or 0x1c10 in PIE)
