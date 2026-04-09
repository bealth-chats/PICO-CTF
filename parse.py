# If 1300 returns the SEED, and it is 16-bit, and I tried 0 to 65535, then what?
# What if the string "SK-CERT" is NOT what `strstr(out, "SK-CERT")` matches?
# The writeup states: `Expected output: VOID::SECTOR-7::SK-CERT{...}::OK`
# BUT what if the flag prefix changed?!
# What if it's NOT `SK-CERT{`?
# In my C runner I matched ONLY "SK-CERT"!
# What if it prints `VOID::SECTOR-7::flag{...}::OK`?
