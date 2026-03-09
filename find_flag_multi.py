with open("system.out", "rb") as f:
    data = f.read()

# Try searching for picoCTF without assuming 1 byte XOR
for i in range(len(data) - 8):
    chunk = data[i:i+8]
    # see if chunk could be encoded somehow
    # Not going to blindly guess. Let's look at `objdump -s -j .rodata system.out` again.
