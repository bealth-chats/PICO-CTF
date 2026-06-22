from unicorn import *
from unicorn.x86_const import *
from pwn import *
import struct

e = ELF('beacon')
BASE = 0x400000

uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, 32 * 1024 * 1024)
for seg in e.iter_segments():
    if seg.header.p_type == 'PT_LOAD':
        uc.mem_write(BASE + seg.header.p_vaddr, seg.data())

rela_dyn = e.get_section_by_name('.rela.dyn')
if rela_dyn:
    for reloc in rela_dyn.iter_relocations():
        if reloc['r_info_type'] == 8:
            offset = BASE + reloc['r_offset']
            addend = BASE + reloc['r_addend']
            uc.mem_write(offset, struct.pack("<Q", addend))

STACK = 0x80000000
uc.mem_map(STACK, 1024 * 1024)

uc.mem_write(BASE + 0x1360, b'\x31\xc0\xc3')
uc.mem_write(BASE + 0x1460, b'\x31\xc0\xc3')
uc.mem_write(BASE + 0x1239, b'\x0f\x0b')
uc.mem_write(BASE + 0x1251, b'\x0f\x0b')

def hook_mem_invalid(uc, access, address, size, value, user_data):
    aligned = address & ~0xFFF
    try:
        uc.mem_map(aligned, 0x10000)
        return True
    except:
        return False
uc.hook_add(UC_HOOK_MEM_INVALID, hook_mem_invalid)

def hook_memset(uc, address, size, user_data):
    dest = uc.reg_read(UC_X86_REG_RDI)
    val = uc.reg_read(UC_X86_REG_RSI) & 0xFF
    sz = uc.reg_read(UC_X86_REG_RDX)
    uc.mem_write(dest, bytes([val]) * sz)
    rsp = uc.reg_read(UC_X86_REG_RSP)
    ret_addr = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
    uc.reg_write(UC_X86_REG_RSP, rsp + 8)
    uc.reg_write(UC_X86_REG_RAX, dest)
    uc.reg_write(UC_X86_REG_RIP, ret_addr)

uc.hook_add(UC_HOOK_CODE, hook_memset, begin=BASE+0x1070, end=BASE+0x1070)

def solve():
    context = uc.context_save()

    data_backup = {}
    for seg in e.iter_segments():
        if seg.header.p_type == 'PT_LOAD' and (seg.header.p_flags & 2):
            vaddr = BASE + seg.header.p_vaddr
            map_addr = vaddr & ~0xFFF
            map_end = (vaddr + seg.header.p_memsz + 0xFFF) & ~0xFFF
            size = map_end - map_addr
            data_backup[map_addr] = bytes(uc.mem_read(map_addr, size))

    import sys
    print("Brute forcing ALL hashes to find the closest to 0xbf71f73f!")
    for seed in range(0x10000):
        if seed % 0x1000 == 0:
            sys.stdout.write(f"\rTrying seed: {hex(seed)}")
            sys.stdout.flush()

        uc.context_restore(context)
        for addr, data in data_backup.items():
            uc.mem_write(addr, data)

        rsp = STACK + 1024 * 1024 - 0x1000
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RBP, rsp)
        uc.mem_write(rsp - 0x1000, b'\x00' * 0x2000)

        uc.mem_write(BASE + 0x1300, b'\xb8' + struct.pack('<I', seed) + b'\xc3')

        try:
            uc.emu_start(BASE + 0x11dc, BASE + 0x1216, count=5000000)
        except Exception as exc:
            pass

        if uc.reg_read(UC_X86_REG_RIP) == BASE + 0x1216:
            hash_val = struct.unpack("<I", uc.mem_read(rsp + 0x4c + 0x100, 4))[0]
            success = struct.unpack("<I", uc.mem_read(rsp + 0x4c + 0x114, 4))[0]
            if success == 1:
                print(f"\nFOUND SUCCESS BIT! Seed: {hex(seed)}, Hash: {hex(hash_val)}")
                break

            # Print if hash matches exactly
            if hash_val == 0xbf71f73f:
                print(f"\nFound match! Seed: {hex(seed)}")
                break

solve()
