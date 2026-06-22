import struct
import sys
from elftools.elf.elffile import ELFFile

with open("beacon", "rb") as f:
    data = f.read()

    # search for 0xd43a15c5 in little endian
    target = struct.pack("<I", 0xd43a15c5)
    idx = data.find(target)
    if idx != -1:
        print("Found constant at offset", hex(idx))
    else:
        print("Constant not found in entire file")
