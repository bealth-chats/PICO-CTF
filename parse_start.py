# Wait, let's find the start of sub_2d90
with open("disasm_intel.txt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "2d90:" in line:
        for j in range(i-20, i+20):
            print(lines[j], end="")
