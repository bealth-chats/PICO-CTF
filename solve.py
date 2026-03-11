import socket

def interact():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('candy-mountain.picoctf.net', 60262))

    # Read prompt
    print(s.recv(1024).decode())

    # Send password
    s.sendall(b"test\n")
    print(s.recv(1024).decode())

    # Send length
    s.sendall(b"80\n")

    # Read leaked bytes
    output = b""
    while b"Enter your hash" not in output:
        output += s.recv(1024)
        if len(output) > 2000:
            break

    print(output.decode())

    # Compute the hash and send
    s.sendall(b"15237662580160011234\n")

    # Read flag
    flag = s.recv(1024)
    print(flag.decode())

interact()
