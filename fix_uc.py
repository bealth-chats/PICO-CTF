from unicorn import *
from unicorn.x86_const import *
from pwn import *
import struct

e = ELF('beacon')
BASE = 0x400000

def solve():
    uc = Uc(UC_ARCH_X86, UC_MODE_64)

    # map 32MB from BASE
    uc.mem_map(BASE, 32 * 1024 * 1024)

    # write segments
    for seg in e.iter_segments():
        if seg.header.p_type == 'PT_LOAD':
            vaddr = BASE + seg.header.p_vaddr
            uc.mem_write(vaddr, seg.data())

    # relocations
    rela_dyn = e.get_section_by_name('.rela.dyn')
    if rela_dyn:
        for reloc in rela_dyn.iter_relocations():
            if reloc['r_info_type'] == 8: # R_X86_64_RELATIVE
                offset = BASE + reloc['r_offset']
                addend = BASE + reloc['r_addend']
                uc.mem_write(offset, struct.pack("<Q", addend))

    # map stack
    STACK = 0x80000000
    uc.mem_map(STACK, 1024 * 1024)
    uc.reg_write(UC_X86_REG_RSP, STACK + 1024 * 1024 - 0x1000)

    # map fs
    TLS = 0x90000000
    uc.mem_map(TLS, 0x1000)
    uc.mem_write(TLS + 0x28, struct.pack("<Q", 0x1337133713371337))
    try:
        uc.reg_write(UC_X86_REG_FS_BASE, TLS)
    except:
        pass

    # hook invalid memory to auto-map
    def hook_mem_invalid(uc, access, address, size, value, user_data):
        print(f"Invalid access at {hex(address)}")
        # page align
        aligned = address & ~0xFFF
        try:
            uc.mem_map(aligned, 0x10000)
            return True
        except:
            return False

    uc.hook_add(UC_HOOK_MEM_INVALID, hook_mem_invalid)

    out_bytes = []
    def hook_code(uc, address, size, user_data):
        if address == BASE + 0x1c10:
            dl = uc.reg_read(UC_X86_REG_RDX) & 0xFF
            out_bytes.append(dl)

    uc.hook_add(UC_HOOK_CODE, hook_code)

    # test sub_2d90
    try:
        uc.reg_write(UC_X86_REG_RDI, 0x5eed) # Maybe seed is arg1?
        # we need to start at 2d90, stop at 2d68 (ret of something?)
        # Let's just start and see what happens
        uc.emu_start(BASE + 0x2d90, BASE + 0x2e10, count=10000)
    except Exception as exc:
        print("Emulation error:", exc)
        print("RIP:", hex(uc.reg_read(UC_X86_REG_RIP)))

    print(out_bytes)

solve()
