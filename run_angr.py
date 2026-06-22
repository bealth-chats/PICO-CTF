import angr
import claripy

p = angr.Project('beacon', load_options={'auto_load_libs': False})
state = p.factory.entry_state()

# The writeup states:
# 1. emulate sub_2d90
# 2. recover plaintext bytes passed through 0x401c10 (or 0x1c10 in PIE)
# 3. brute-force the 16-bit seed
# 4. stop when internal hash matches 0xd43a15c5

# Wait, if we use Unicorn and simply loop through 0..65535, it's very fast.
# Our Unicorn script had an issue with segment mapping. Let's fix that.
