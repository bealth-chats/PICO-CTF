from unicorn import *
from unicorn.x86_const import *
from pwn import *
import struct
import concurrent.futures

e = ELF('beacon')
BASE = 0x400000

def worker(start_seed, end_seed):
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

    # Patch anti-debug
    uc.mem_write(BASE + 0x1360, b'\x31\xc0\xc3')
    uc.mem_write(BASE + 0x1460, b'\x31\xc0\xc3')

    context = uc.context_save()

    data_backup = {}
    for seg in e.iter_segments():
        if seg.header.p_type == 'PT_LOAD' and (seg.header.p_flags & 2):
            vaddr = BASE + seg.header.p_vaddr
            map_addr = vaddr & ~0xFFF
            map_end = (vaddr + seg.header.p_memsz + 0xFFF) & ~0xFFF
            size = map_end - map_addr
            data_backup[map_addr] = bytes(uc.mem_read(map_addr, size))

    for seed in range(start_seed, end_seed):
        uc.context_restore(context)
        for addr, data in data_backup.items():
            uc.mem_write(addr, data)

        rsp = STACK + 1024 * 1024 - 0x1000
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RBP, seed)
        uc.mem_write(rsp - 0x1000, b'\x00' * 0x2000)

        try:
            uc.emu_start(BASE + 0x1200, BASE + 0x1216, count=5000000)
        except Exception as exc:
            pass

        if uc.reg_read(UC_X86_REG_RIP) == BASE + 0x1216:
            hash_val = struct.unpack("<I", uc.mem_read(rsp + 0x4c + 0x100, 4))[0]
            if hash_val == 0xbf71f73f:
                return (seed, bytes(uc.mem_read(rsp + 0x4c, 0x200)))
            if seed % 0x100 == 0:
                with open(f"hash_log.txt", "a") as f:
                    f.write(f"Seed {hex(seed)}: {hex(hash_val)}\n")
    return None

if __name__ == '__main__':
    open("hash_log.txt", "w").write("") # clear log
    step = 65536 // 32
    ranges = [(i, i+step) for i in range(0, 65536, step)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(worker, r[0], r[1]): r for r in ranges}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                with open("found_seed.txt", "w") as f:
                    f.write(hex(res[0]))
                with open("ctx_dump.bin", "wb") as f:
                    f.write(res[1])
                print(f"FOUND! {hex(res[0])}")
                import sys
                sys.exit(0)
    print("Done")
