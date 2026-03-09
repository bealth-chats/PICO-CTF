from scapy.all import *

packets = rdpcap('rogue_tower.pcap')
for p in packets:
    if p.haslayer(TCP) and p.haslayer(Raw):
        payload = bytes(p[TCP].payload)
        if b'HTTP' in payload or b'POST' in payload or b'GET' in payload:
            print(f"{p[IP].src} -> {p[IP].dst}")
            print(payload.decode('utf-8', errors='ignore'))
            print("-" * 50)
