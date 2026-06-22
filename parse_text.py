with open("disasm_intel.txt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "d43a15c5" in line.lower() or "c5 15 3a d4" in line.lower():
        print(lines[i-2].strip())
        print(lines[i-1].strip())
        print(line.strip())
        print(lines[i+1].strip())
        print(lines[i+2].strip())
        print("---")
