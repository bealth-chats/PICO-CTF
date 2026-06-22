from unicorn import *
from unicorn.x86_const import *
from pwn import *
import struct

e = ELF('beacon')

# memory
BASE = 0x400000
CODE_SIZE = 0x2000000
STACK_ADDR = 0x8000000
STACK_SIZE = 0x100000

def solve(seed):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(BASE, CODE_SIZE)
    uc.mem_map(STACK_ADDR, STACK_SIZE)

    uc.mem_write(BASE, e.get_data())

    # apply relocations
    uc.mem_write(BASE + 0x1107040, struct.pack("<Q", BASE + 0x1107040))

    # setup stack
    rsp = STACK_ADDR + STACK_SIZE - 0x1000
    uc.reg_write(UC_X86_REG_RSP, rsp)

    # how to find sub_2d90? It's mentioned as the key gate.
    pass

solve(0x5eed)
