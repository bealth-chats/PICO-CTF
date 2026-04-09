from unicorn import *
from unicorn.x86_const import *
from pwn import *
import struct

e = ELF('beacon')

BASE = 0x4000000
CODE_SIZE = 0x100000
STACK_ADDR = 0x8000000
STACK_SIZE = 0x100000

# Writeup: hook the internal output helper at 0x401c10 -> wait, 0x401c10
# So sub_2d90 is at 0x402d90

def solve(seed):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(BASE, CODE_SIZE)
    uc.mem_map(STACK_ADDR, STACK_SIZE)

    # Load all PT_LOAD segments
    for seg in e.iter_segments():
        if seg.header.p_type == 'PT_LOAD':
            vaddr = BASE + seg.header.p_vaddr
            memsz = seg.header.p_memsz
            filesz = seg.header.p_filesz

            # Map memory with page alignment
            map_addr = vaddr & ~0xFFF
            map_size = (vaddr + memsz - map_addr + 0xFFF) & ~0xFFF
            try:
                uc.mem_map(map_addr, map_size)
            except:
                pass

            uc.mem_write(vaddr, seg.data())

    # apply relative relocations
    rela_dyn = e.get_section_by_name('.rela.dyn')
    if rela_dyn:
        for reloc in rela_dyn.iter_relocations():
            if reloc['r_info_type'] == 8: # R_X86_64_RELATIVE
                offset = BASE + reloc['r_offset']
                addend = BASE + reloc['r_addend']
                uc.mem_write(offset, struct.pack("<Q", addend))

    # set up stack
    rsp = STACK_ADDR + STACK_SIZE - 0x1000
    uc.reg_write(UC_X86_REG_RSP, rsp)

    # Need FS canary area
    # Allocate a page for TLS
    TLS_ADDR = 0x9000000
    uc.mem_map(TLS_ADDR, 0x1000)

    # Set FS base
    import urllib.request
    # Actually wait, let's use MSR
    # uc.reg_write(UC_X86_REG_FS_BASE, TLS_ADDR) # This might not work directly, need to set MSR

    uc.mem_write(TLS_ADDR + 0x28, struct.pack("<Q", 0x4141414141414141)) # Canary

    uc.reg_write(UC_X86_REG_RDI, seed) # arg 1? Wait, seed brute force.

    out_bytes = []

    def hook_code(uc, address, size, user_data):
        if address == BASE + 0x1c10:
            dl = uc.reg_read(UC_X86_REG_RDX) & 0xFF
            out_bytes.append(dl)

    uc.hook_add(UC_HOOK_CODE, hook_code)

    # We need to emulate sub_2d90
    try:
        uc.emu_start(BASE + 0x2d90, BASE + 0x2d90 + 0x1000) # Actually we need the end of sub_2d90
    except Exception as exc:
        print("Emulation error:", exc)
        print("RIP:", hex(uc.reg_read(UC_X86_REG_RIP)))

    print(out_bytes)

solve(0x5eed)
