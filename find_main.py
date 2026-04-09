from pwn import *
e = ELF('beacon')
print("Entry point:", hex(e.entry))
