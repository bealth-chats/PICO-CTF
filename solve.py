# The hint says "The answer is in the .rodata section and the 18-entry function pointer table."
# 18-entry function pointer table is at 0x1106d50 (in memory 0x406d50 or whatever, but actually we extracted it:
# 2170, 21f0, 2270, 22f0, 2370, 23f0, 2470, 24f0, 2570, 2600, 2690, 2720, 27a0, 2830, 28c0, 2950, 4090, 40e0).
# In each of these 18 functions, there is a XOR against a value loaded from .rodata:
# 0x2170 XOR eax, dword ptr [rip + 0x1104f13]
# We extracted those addresses:
# 0x11070b8, 0x11070c0, ... 0x1107210, 0x1107218. Wait, these were in .data or .bss!
# But wait...
# "The answer is in the .rodata section"
# If we look at the exact .rodata addresses being referenced in the functions:
# 0x2170 XOR eax, dword ptr [rip + 0x1104f13]
# rip = 0x21a5 -> 0x21a5 + 0x1104f13 = 0x11070b8. This is .bss?
pass
