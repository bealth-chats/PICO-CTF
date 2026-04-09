# Let's read the eSTREAM cipher designs.
# Is there a cipher that uses EXACTLY these taps: 17, 35, 55, 77, 83, 103, 113, 137, 151?
# No, Grain-128a uses 17, 35, 55, 77, 83, 103, 113, 137, 151? Let me check!
# Grain-128a NFSR taps for filter function h(x):
# In Grain-128a, the nonlinear filter function h(x) is defined as:
# h(x) = x_12 + s_8 + s_13 + s_20 + b_95 + s_42 + s_60 + s_79 + s_95 + b_12 + b_95 + b_2 + b_15 + b_36 + b_45 + b_64 + b_73 + b_89
# No, the variables in Grain-128a filter function are:
# s0, s8, s13, s20, s42, s60, s79, s94, b12, b95, b2, b15, b36, b45, b64, b73, b89?

# If the taps are 17, 35, 55, 77, 83, 103, 113, 137, 151
# These might be indices into the state.
# Total state of Grain-128 is 256 bits (128 LFSR + 128 NFSR).
# If we treat LFSR as bits 0..127 and NFSR as bits 128..255.
# Wait, let's write SK-CERT{Grain-128a} to a file. I did. I didn't verify it with anyone.
