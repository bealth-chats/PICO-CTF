# picoCTF - Compare is API too

## Challenge Description
The executable was designed to send the flag to someone. Are you that someone?
Hint: Frida is a great starting point.
Compare is API too...

## Analysis
The provided file is `bin-ins.exe`. Running initial string analysis and checking exports/imports shows it's a 64-bit Windows PE.

If we look at the binary with LIEF or `objdump`, it contains a suspicious `.ATOM` section.
```
objdump -h bin-ins.exe
```

A manual analysis of the code at `140001dc0` reveals a PE loader. The binary reads the `.ATOM` section, extracts it (it turns out to be LZMA-compressed data, as decompressed by a function tracing back to `140001300`), and maps the inner PE file into memory.

Dumping the `.ATOM` section and decompressing it using `xz`:
```bash
xz -d < atom.bin > extracted_pe.bin
```
This gives us a new executable.

If we inspect `extracted_pe.bin`, we find that it imports `msvcrt.dll` functions and networking APIs (`WS2_32.dll`). It's a network client that prints `Enter the key: `, reads user input, sends it via a socket (`send`), receives data, constructs a string, and then compares the key using `lstrcmpA`.

The flag is constructed inside this binary. The inner binary uses global constructors to populate an array `_ZL9flagParts` with pieces of the flag. This initialization happens in `_Z41__static_initialization_and_destruction_0ii` around `0x401b5c`.

Looking at the disassembly, we see it adds string fragments using `std::string` piecewise construction from `.rdata` offsets:
```
0x4b30b6: "cGljb0NURnt"
0x4b30c2: "uM3R3MHJrXz"
0x4b30ce: "FzXzRQMXNfN"
0x4b30da: "FNfVzMxMV85"
0x4b30e6: "ZTYwZGVlNH0K"
```

Concatenating these fragments yields:
`cGljb0NURntuM3R3MHJrXzFzXzRQMXNfNFNfVzMxMV85ZTYwZGVlNH0K`

Base64 decoding this gives the final flag:
```
picoCTF{n3tw0rk_1s_4P1s_4S_W311_9e60dee4}
```

The initial hypothesis of `strncmp` being hooked was a red herring or part of the obfuscation from the outer PE to load the binary properly, or it intercepted network communication in some way. However, statically dumping and reversing the embedded binary allowed us to completely bypass any dynamic checks and simply read the base64 encoded flag from memory.
