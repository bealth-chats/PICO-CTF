# CTF Writeup

## Challenge Description
We recovered a suspicious packet capture file (`packets.pcap`) that seems to contain a transferred file. The sender was kind enough to also share the script they used to encode and send it (`encrypt.py`). Can you reconstruct the original file?

## Analysis

### 1. Analyzing the Encoding Script (`encrypt.py`)
The provided script `encrypt.py` simulates a file transfer and shows how each byte of the file was encoded before being sent.

```python
def encode_byte(b, key):
    return (b + key) % 256
```

The script uses a default key of `42`. To reverse this encoding, we simply need to subtract `42` from each byte and take the result modulo `256`. The decoding function would look like this:

```python
def decode_byte(b, key):
    return (b - key) % 256
```

### 2. Extracting Data from the PCAP (`packets.pcap`)
We analyzed the `packets.pcap` file using `scapy`. The file contains TCP packets. We can extract the payload from the raw data layer of the relevant TCP packets. Looking at the PCAP, the data transfer occurred between ports `12345` (source) and `9000` (destination).

We used the following script to extract and order the payloads based on their TCP sequence numbers, and then decode the bytes:

```python
from scapy.all import rdpcap, TCP, Raw

pkts = rdpcap("packets.pcap")
payloads = {}

# Extract payloads
for p in pkts:
    if p.haslayer(TCP) and p.haslayer(Raw):
        if p[TCP].sport == 12345 and p[TCP].dport == 9000:
            payloads[p[TCP].seq] = p[Raw].load

data = b""
# Order payloads by sequence number to ensure correct data reconstruction
for seq in sorted(payloads.keys()):
    data += payloads[seq]

# Decode the extracted data
key = 42
decoded = bytes([(b - key) % 256 for b in data])

# Write the reconstructed file
with open("decoded.jpg", "wb") as f:
    f.write(decoded)
```

### 3. Recovering the Original File
Running the extraction script resulted in a file `decoded.jpg`. Checking the file type confirms it is a JPEG image:
```bash
$ file decoded.jpg
decoded.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 800x500, components 3
```

Opening the reconstructed image reveals the flag.

## Flag
`picoCTF{tr4ck_th3_tr4ff1c_0c09bb9e}`
