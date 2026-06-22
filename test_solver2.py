from unicorn import *
from unicorn.x86_const import *
from pwn import *
import struct

e = ELF('beacon')

BASE = 0x4000000
STACK_ADDR = 0x8000000
STACK_SIZE = 0x100000

def solve(seed):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
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

            # Write data
            try:
                uc.mem_write(vaddr, seg.data())
            except Exception as exc:
                print("Error writing segment at", hex(vaddr), ":", exc)

    # apply relative relocations
    rela_dyn = e.get_section_by_name('.rela.dyn')
    if rela_dyn:
        for reloc in rela_dyn.iter_relocations():
            if reloc['r_info_type'] == 8: # R_X86_64_RELATIVE
                offset = BASE + reloc['r_offset']
                addend = BASE + reloc['r_addend']
                try:
                    uc.mem_write(offset, struct.pack("<Q", addend))
                except:
                    pass

    # set up stack
    rsp = STACK_ADDR + STACK_SIZE - 0x1000
    uc.reg_write(UC_X86_REG_RSP, rsp)
    uc.reg_write(UC_X86_REG_RBP, rsp)

    # Need FS canary area
    TLS_ADDR = 0x9000000
    uc.mem_map(TLS_ADDR, 0x1000)

    # Set FS base
    import sys
    sys.path.append("/usr/lib/python3/dist-packages")
    # https://github.com/unicorn-engine/unicorn/issues/1360
    # There is no direct FS_BASE register in older unicorn, we need to use MSR
    # or just use UC_X86_REG_FS_BASE if available
    try:
        uc.reg_write(UC_X86_REG_FS_BASE, TLS_ADDR)
    except:
        uc.reg_write(UC_X86_REG_MSR, 0xC0000100) # FS_BASE
        uc.reg_write(UC_X86_REG_MSR, TLS_ADDR) # Actually not how MSR writes work in Unicorn...

    # setup seed
    # "derive a 16-bit seed from ptrace" - so the seed might be in a register.
    # We will put it in RDI
    uc.reg_write(UC_X86_REG_RDI, seed)

    out_bytes = []

    def hook_code(uc, address, size, user_data):
        if address == BASE + 0x1c10:
            dl = uc.reg_read(UC_X86_REG_RDX) & 0xFF
            out_bytes.append(dl)
            # print("Intercepted byte:", hex(dl))

    uc.hook_add(UC_HOOK_CODE, hook_code)

    # Let's see where sub_2d90 ends by disassembling it
    try:
        uc.emu_start(BASE + 0x2d90, BASE + 0x2e10)
    except Exception as exc:
        print("Emulation error:", exc)
        print("RIP:", hex(uc.reg_read(UC_X86_REG_RIP)))

    print(out_bytes)

solve(0x5eed)
