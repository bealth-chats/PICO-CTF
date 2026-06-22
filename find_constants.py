import struct
from elftools.elf.elffile import ELFFile

with open("beacon", "rb") as f:
    elf = ELFFile(f)
    code = elf.get_section_by_name(".text").data()
    offset = elf.get_section_by_name(".text").header['sh_offset']
    addr = elf.get_section_by_name(".text").header['sh_addr']

    # search for 0xd43a15c5 in little endian
    target = struct.pack("<I", 0xd43a15c5)
    idx = code.find(target)
    if idx != -1:
        print("Found constant at offset", hex(idx), "address", hex(addr + idx))
    else:
        print("Constant not found in .text")
