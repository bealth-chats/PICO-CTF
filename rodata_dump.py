with open("beacon", "rb") as f:
    f.seek(0x5000)
    data = f.read(0x1000)
    print(data[:256].hex())
