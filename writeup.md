# Writeup: Network Printer Challenge

## Problem Description
Oops! Someone accidentally sent an important file to a network printer—can you retrieve it from the print server?
The printer is on `49354`.
You can try `$ nc -vz mysterious-sea.picoctf.net 49354`.

## Solution Steps

1. **Initial Connectivity Check**:
   I verified connectivity to the target on the specified port using `nc` and it successfully connected:
   ```bash
   $ nc -vz mysterious-sea.picoctf.net 49354
   Connection to mysterious-sea.picoctf.net (3.130.79.223) 49354 port [tcp/*] succeeded!
   ```

2. **Service Enumeration**:
   To determine what type of service is actually running on port 49354, I used `nmap`:
   ```bash
   $ nmap -sV -p 49354 mysterious-sea.picoctf.net
   ```
   The `nmap` scan revealed that the port is actually hosting a **Samba smbd** service, specifically version 4.6.2.

3. **Listing Samba Shares**:
   Given that a Samba service is exposed, I attempted to list the available network shares on this server using `smbclient` with an anonymous login (`-N`):
   ```bash
   $ smbclient -L //mysterious-sea.picoctf.net -p 49354 -N
   ```
   This command successfully connected and listed a share named `shares` with a comment "Public Share With Guests".

4. **Accessing the Share**:
   I then connected to the `shares` share directly to view its contents:
   ```bash
   $ smbclient //mysterious-sea.picoctf.net/shares -p 49354 -N -c "ls"
   ```
   The directory listing returned:
   ```
     .                                   D        0  Fri Mar  6 20:25:42 2026
     ..                                  D        0  Fri Mar  6 20:25:42 2026
     dummy.txt                           N     1142  Wed Feb  4 21:22:17 2026
     flag.txt                            N       37  Fri Mar  6 20:25:42 2026
   ```

5. **Retrieving the Flag**:
   I saw a file named `flag.txt` inside the share. I downloaded it to the local machine:
   ```bash
   $ smbclient //mysterious-sea.picoctf.net/shares -p 49354 -N -c "get flag.txt"
   ```

6. **Reading the Flag**:
   Finally, I read the contents of the downloaded `flag.txt`:
   ```bash
   $ cat flag.txt
   picoCTF{5mb_pr1nter_5h4re5_9fc5e085}
   ```

## Flag
`picoCTF{5mb_pr1nter_5h4re5_9fc5e085}`
