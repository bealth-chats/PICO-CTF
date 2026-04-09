# TRIVIUM uses a 288-bit state.
# 288 bits, divided into 3 shift registers of length 93, 84, and 111 bits.
# Total is 288.
# Taps are at bits:
# 65, 92, 90, 91 (for first register, length 93)
# 161, 176, 174, 175 (for second register, length 84, indices 93 to 176) -> 161-93 = 68, 176-93=83, 174-93=81, 175-93=82
# 242, 287, 285, 286 (for third register, length 111, indices 177 to 287) -> 242-177=65, 287-177=110, 285-177=108, 286-177=109
# None of these are 17, 35, 55...

# What about Mickey v2?
# Mickey-128?
# Mickey v2 state update uses taps:
# 17, 35, 55, 77, 83, 103, 113, 137, 151
# WAIT!!!
# Let's check MICKEY v2!
# Mickey v2 is a stream cipher based on two 100-bit registers (R and S).
# For Mickey-128, the registers are 160 bits each.
# Taps for Mickey-128: 17, 35, 55, 77, 83, 103, 113, 137, 151.
# ARE THESE EXACTLY THE TAPS FOR MICKEY-128?
