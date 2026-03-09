# picoCTF - Zip and Split Files

## Challenge Description
After logging in, you will find multiple file parts in your home directory. These parts need to be combined and extracted to reveal the flag.

SSH to dolphin-cove.picoctf.net:63451 and login as ctf-player with password 8d076785.

## Solution

1. **Connect via SSH:**
   Connect to the server using the provided credentials.
   ```bash
   ssh -p 63451 ctf-player@dolphin-cove.picoctf.net
   # Password: 8d076785
   ```

2. **Examine the Files:**
   Listing the files in the directory reveals `instructions.txt` and several split file parts:
   `part_aa`, `part_ab`, `part_ac`, `part_ad`, `part_ae`.

   Reading `instructions.txt` gives the following hint:
   > - The flag is split into multiple parts as a zipped file.
   > - Use Linux commands to combine the parts into one file.
   > - The zip file is password protected. Use this "supersecret" password to extract the zip file.
   > - After unzipping, check the extracted text file for the flag.

3. **Combine the Parts:**
   We can combine the split parts into a single zip file using `cat`:
   ```bash
   cat part_a* > combined.zip
   ```

4. **Extract the Zip File:**
   The hint mentions the password is "supersecret". We unzip the combined file using:
   ```bash
   unzip -P supersecret combined.zip
   ```
   This extracts a file named `flag.txt`.

5. **Read the Flag:**
   Finally, we view the contents of `flag.txt`:
   ```bash
   cat flag.txt
   ```

## Flag
`picoCTF{z1p_and_spl1t_f1l3s_4r3_fun_4e5c49a8}`