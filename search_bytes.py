with open("beacon", "rb") as f:
    data = f.read()

import struct
target = struct.pack("<I", 0xd43a15c5)
idx = data.find(target)
print("target", target.hex(), "idx", idx)
