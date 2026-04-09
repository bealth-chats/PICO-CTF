import subprocess

lines = subprocess.check_output("objdump -M intel -d beacon", shell=True).decode().splitlines()

# Search for the function that intercepts the plaintext bytes
# "That helper receives each plaintext byte in RDX."
for i, line in enumerate(lines):
    if "mov" in line and "dl" in line and "byte ptr" in line.lower():
        print("Found potentially what we want at: " + line)
