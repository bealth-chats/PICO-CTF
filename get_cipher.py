# The user hint: "The flag itself is the name of the cipher — look up "Grain-128" and think about what "state coupling" and "nonlinearity" mean in stream cipher design. The answer is in the .rodata section and the 18-entry function pointer table."
# Could "The answer is in the .rodata section AND the 18-entry function pointer table" mean something more literal?
# 18-entry function pointer table...
# And the .rodata section...
# 9 function pointers for R taps: 17, 35, 55, 77, 83, 103, 113, 137, 151
# What about the S taps?
# 0x2170 XOR esi, 7
# 0x21f0 XOR esi, 0x19 (25)
# 0x2270 XOR esi, 0xd  (13)
# 0x22f0 XOR esi, 0x13 (19)
# 0x2370 (none) -> 0
# 0x23f0 XOR esi, 9
# 0x2470 XOR esi, 0x15 (21)
# 24f0 XOR esi, 0x1b (27)
# 2570 XOR esi, 3
# 2600 XOR esi, 0xf  (15)
# 2690 XOR esi, 0x11 (17)
# 2720 XOR esi, 0x17 (23)
# 27a0 XOR esi, 0x1b (27)
# 2830 XOR esi, 1
# 28c0 XOR esi, 7
# 2950 XOR esi, 0xb  (11)

# MICKEY-128 2.0 has two variants: MICKEY 2.0 (80 bit) and MICKEY-128 2.0 (128 bit key).
# What are the exact names used by eSTREAM?
# MICKEY-128 2.0
# Or maybe the flag is SK-CERT{MICKEY-128 2.0}?
pass
