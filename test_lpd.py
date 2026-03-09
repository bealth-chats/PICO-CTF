import socket

host = "mysterious-sea.picoctf.net"
port = 49354

for i in range(1, 6):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))

        # LPD commands
        cmd = bytes([i]) + b'lp\n'
        print(f"Sending {cmd}")
        s.send(cmd)

        response = s.recv(4096)
        print(f"Response for {i}:", response)
        s.close()
    except Exception as e:
        print(f"Error for {i}: {e}")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((host, port))

    # Just try getting whatever
    s.send(b'\n')

    response = s.recv(4096)
    print("Response for newline:", response)
    s.close()
except Exception as e:
    print(e)
