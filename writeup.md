# Forensics CTF Challenge Write-up

## Challenge Description
"This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this?"

## Files Given
- `digits.bin`

## Solution Steps

1. **Analyze the input file:**
   We start by examining the contents of `digits.bin`. It is a large text file containing only the characters `0` and `1`.
   ```bash
   head digits.bin
   ```
   Checking the size of the file:
   ```bash
   wc -c digits.bin
   ```
   The file contains exactly 71,096 characters (bits).

2. **Convert bits to bytes:**
   Since 71,096 is perfectly divisible by 8, it strongly suggests that the sequence of bits is actually a byte stream where each group of 8 bits represents a single byte.

   We can write a simple Python script to read the binary string, chunk it into 8-bit pieces, convert each to an integer, and write out the resulting bytes to a new file:

   ```python
   with open("digits.bin", "r") as f:
       data = f.read().strip()

   # Group by 8 bits and convert to bytes
   bytes_data = [int(data[i:i+8], 2) for i in range(0, len(data), 8)]

   # Write to an output file
   with open("out.bin", "wb") as f:
       f.write(bytes(bytes_data))
   ```

3. **Identify the resulting file type:**
   After running the script, we get a new binary file named `out.bin`. Let's use the `file` command to see what type of file we recovered:
   ```bash
   file out.bin
   ```
   The output reveals that the file is actually a JPEG image:
   `out.bin: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 800x500, components 3`

4. **Extract the flag:**
   We can rename `out.bin` to `out.jpg` and open it in an image viewer.
   ```bash
   mv out.bin out.jpg
   ```

   Looking at the image, the flag is clearly visible as red text on a white background.

## Flag
`picoCTF{h1dd3n_1n_th3_b1n4ry_a59b2b0a}`