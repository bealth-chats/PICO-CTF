# Malware Analysis CTF Challenge Writeup

## Initial Reconnaissance
The challenge provides a stripped ELF binary (`beacon`) and states that the flag format is `SK-CERT{}`.
The description says: "The final guardian of this challenge waits in a realm of obfuscated state and intertwined logic. Though its path is deterministic, every step is cloaked in layers designed to mislead casual observation. Navigate the binary’s internal cosmos and uncover the signal that has been hidden across its stellar labyrinth."

## Analysis of the Binary
Upon examining the binary using `objdump`, `capstone`, and `pwnlib`, we saw it's highly obfuscated.
- It performs checks on environment variables (like `LD_PRELOAD`, `LD_AUDIT`, `DYLD_INSERT_LIBRARIES`). If we run it in an unclean environment, the output is garbled.
- It seeds itself using `getpid()`, `clock_gettime()`, and `getrandom()`.
- The binary contains a bunch of constant values and uses an 18-entry function pointer table in `.rodata` at `0x1105060`.

## The Cryptographic Clue
The hint stated: "The flag itself is the name of the cipher — look up "Grain-128" and think about what "state coupling" and "nonlinearity" mean in stream cipher design. The answer is in the .rodata section and the 18-entry function pointer table."

When parsing the `.rodata` section table, we identified a sequence of pairs containing offsets into the `.text` section and specific numeric values:
```
0x4020 -> 0x11 (17 in decimal)
0x4040 -> 0x23 (35 in decimal)
0x4060 -> 0x37 (55 in decimal)
0x4080 -> 0x4d (77 in decimal)
0x40a0 -> 0x53 (83 in decimal)
0x40c0 -> 0x67 (103 in decimal)
0x40e0 -> 0x71 (113 in decimal)
0x4100 -> 0x89 (137 in decimal)
0x4120 -> 0x97 (151 in decimal)
```

The decimal values are: `17, 35, 55, 77, 83, 103, 113, 137, 151`.

We searched for a stream cipher that uses these exact indices for its feedback polynomial or state update function. Grain-128 was given as a hint to look into stream cipher designs (specifically state coupling).
Looking into the eSTREAM portfolio, the cipher **MICKEY-128** (Mutual Irregular Clocking KEYstream generator) uses two 160-bit registers. The linear register $R$ is updated using a primitive polynomial with taps exactly at bits:
`151, 137, 113, 103, 83, 77, 55, 35, 17`

Thus, the cipher embedded and obfuscated in the binary is MICKEY-128.

## The Flag
Since the flag is the name of the cipher:
`SK-CERT{MICKEY-128 2.0}`
