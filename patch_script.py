from pwn import *
import ctypes

# If Unicorn fails because of unmapped memory when executing 0x2d90,
# maybe we can just use ctypes? The ELF is a shared library (PIE).
# We can load it with ctypes.CDLL.
# The entry point sub_2d90 is at offset 0x2d90.

lib = ctypes.CDLL('./beacon')

print("Loaded beacon")
# We need to call the initialization functions, or better, we can patch `main` to brute force the seed.
