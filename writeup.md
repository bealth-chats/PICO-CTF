# Rogue Tower CTF Write-up

## Challenge Description
A suspicious cell tower has been detected in the network. Analyze the captured network traffic to identify the rogue tower, find the compromised device, and recover the exfiltrated flag.

## Hints
* Look for unauthorized test network broadcasts on UDP port 55000
* Find the device that connected to the rogue tower by checking HTTP User-Agent headers
* The encryption key is derived from the victim device's IMSI
* The exfiltrated data is split across multiple HTTP POST requests

## Solution Steps

### 1. Identify the Rogue Tower
The first hint suggested looking at UDP broadcasts on port 55000. Using Python and Scapy, we can inspect these packets:

```python
from scapy.all import *

packets = rdpcap('rogue_tower.pcap')
for p in packets:
    if p.haslayer(UDP) and (p[UDP].dport == 55000 or p[UDP].sport == 55000):
        print(p.summary())
        print(bytes(p[UDP].payload))
```

The output reveals three broadcasts:
* `b'CARRIER: Verizon PLMN=310410 CELLID=21964'`
* `b'CARRIER: AT&T PLMN=310410 CELLID=21965'`
* `b'UNAUTHORIZED-TEST-NETWORK PLMN=00101 CELLID=97726 '`

From this, we can conclude that the rogue tower's **CELLID is 97726**.

### 2. Find the Compromised Device
Next, we need to find the device that connected to this rogue tower. We can search HTTP traffic for the User-Agent headers connecting to CELLID 97726.

```python
for p in packets:
    if p.haslayer(TCP) and p.haslayer(Raw):
        payload = bytes(p[TCP].payload)
        if b'HTTP' in payload or b'POST' in payload or b'GET' in payload:
            print(f"{p[IP].src} -> {p[IP].dst}")
            print(payload.decode('utf-8', errors='ignore'))
```

Looking through the output, we find the following HTTP GET request:
```
10.100.55.55 -> 198.51.100.244
GET /api/register HTTP/1.1
Host: network.carrier.com
User-Agent: MobileDevice/1.0 (IMSI:310410275849303; CELL:97726)
Accept: */*
Connection: close
```
This request confirms that a device with the **IMSI `310410275849303`** successfully connected to our rogue tower. It also gives us the IP address of the rogue tower (`198.51.100.244`).

### 3. Extract the Exfiltrated Data
The hints say the data was split across multiple POST requests. Looking at the traffic directed to the rogue tower (`198.51.100.244`), we find several POST requests to `/upload` sending pieces of data:
```
R1xbW3pnd
khFBV9BCm
xTAFtZZ0A
JRANBaAIB
BloEAQUAS
A==
```

Concatenating these together gives us a complete base64 encoded string: `R1xbW3pndkhFBV9BCmxTAFtZZ0AJRANBaAIBBloEAQUASA==`.

### 4. Decrypt the Data
The hint specifies the key is derived from the IMSI. We have the IMSI: `310410275849303`. We can decode the base64 payload and write a simple script to try XOR decryption. Since the key is "derived from the victim device's IMSI", we can test what the key needs to be to produce `picoCTF{` for the first 8 characters.

```python
import base64

data = "R1xbW3pndkhFBV9BCmxTAFtZZ0AJRANBaAIBBloEAQUASA=="
decoded = base64.b64decode(data)

expected = b"picoCTF{"

for i in range(len(expected)):
    print(chr(decoded[i] ^ expected[i]), end="")
print()
```

The output gives us: `75849303`. This happens to be the last 8 digits of the victim's IMSI `310410275849303`.

Knowing the key is `75849303`, we can write the final decryption script:

```python
import base64

data = "R1xbW3pndkhFBV9BCmxTAFtZZ0AJRANBaAIBBloEAQUASA=="
decoded = base64.b64decode(data)

key = b"75849303"

flag = ""
for i in range(len(decoded)):
    flag += chr(decoded[i] ^ key[i % len(key)])
print(flag)
```

Running this script reveals the flag!

**Flag:** `picoCTF{r0gu3_c3ll_t0w3r_792c7167}`
