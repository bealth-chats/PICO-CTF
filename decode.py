from scapy.all import rdpcap, TCP, Raw

pkts = rdpcap("packets.pcap")
payloads = {}
for p in pkts:
    if p.haslayer(TCP) and p.haslayer(Raw):
        if p[TCP].sport == 12345 and p[TCP].dport == 9000:
            payloads[p[TCP].seq] = p[Raw].load

data = b""
for seq in sorted(payloads.keys()):
    data += payloads[seq]

decoded = bytes([(b - 42) % 256 for b in data])

with open("decoded.out", "wb") as f:
    f.write(decoded)
