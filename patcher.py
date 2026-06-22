from pwn import *

# Let's bypass anti-analysis directly.
# 1349:	66 85 c0             	test   ax,ax
# 134c:	b9 01 00 00 00       	mov    ecx,0x1
# 1351:	0f 44 c1             	cmove  eax,ecx

# Let's just find the comparisons with anti-analysis and nop them or patch them.
# Even better: patch the call to write!
# 12df: e8 6c fd ff ff       call   1050 <write@plt>
# What if we patch `main` so that at 12df, it prints our buffer.
# But `main` only generates the buffer for the SEED it obtains from ptrace.
# Wait, "derive a 16-bit seed from ptrace". The binary does this at runtime.
# But under a debugger, or without ptrace TRACEME succeeding, it might use a bad seed or fail.

e = ELF('beacon')
print(e.entry)
