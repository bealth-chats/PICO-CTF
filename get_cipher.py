# Let's search the .rodata section for the string starting with SK-CERT{
import re
data = open('beacon', 'rb').read()
match = re.search(b'SK-CERT{[^}]+}', data)
if match:
    print(match.group(0))
else:
    print("Not found as plain text")
