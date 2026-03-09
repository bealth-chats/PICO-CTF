# picoCTF Forensics Challenge Writeup

## Description
Can you find the flag in this disk image? This time I deleted the file! Let see you get it now!

## Hint
How would you look for deleted files?

## Solution Steps

1. **Extract the Disk Image:**
   The challenge provides a compressed disk image file named `disko-4.dd.gz`. First, I extracted it using `gunzip`:
   ```bash
   gunzip -c disko-4.dd.gz > disko-4.dd
   ```

2. **Analyze the File System:**
   To analyze the file system and look for deleted files, I used tools from the `sleuthkit` package. First, I verified the file system type and structure using `file`:
   ```bash
   file disko-4.dd
   ```
   This indicated it was a DOS/MBR boot sector with a FAT32 filesystem.

3. **List Files (including deleted ones):**
   I used the `fls` command from `sleuthkit` to list files recursively in the image. I was particularly looking for files marked with `*` which indicates they have been deleted.
   ```bash
   fls -r disko-4.dd
   ```
   Scanning the output, I found a suspiciously named deleted file at the bottom:
   ```
   + r/r * 532021:	dont-delete.gz
   ```
   The `*` confirms it was deleted, and its inode number is `532021`.

4. **Recover the Deleted File:**
   Knowing the inode number, I used `icat` to extract the contents of the deleted file `dont-delete.gz` and saved it to my local filesystem:
   ```bash
   icat disko-4.dd 532021 > dont-delete.gz
   ```

5. **Extract the Flag:**
   Finally, since the recovered file is a gzip archive, I used `zcat` to read its contents directly:
   ```bash
   zcat dont-delete.gz
   ```

## Flag
```
picoCTF{d3l_d0n7_h1d3_w3ll_c2fcb641}
```
