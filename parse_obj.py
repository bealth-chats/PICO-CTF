import subprocess
out = subprocess.check_output("objdump -d beacon", shell=True).decode()
for line in out.splitlines():
    if "c5 15 3a d4" in line or "d43a15c5" in line:
        print(line)
