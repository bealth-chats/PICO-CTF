# picoCTF - Bythemancy 0

## Challenge Description

Can you conjure the right bytes? The program's source code can be downloaded here.
Connect to the program with netcat:
`$ nc candy-mountain.picoctf.net 61433`

## Solution

The challenge requires connecting to a remote server using netcat or a simple socket script.

1.  **Connect to the server:** Let's look at the output when connecting to `candy-mountain.picoctf.net` on port `61433`.

    ```
    ⊹──────[ BYTEMANCY-0 ]──────⊹
    ☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐

    Send me ASCII DECIMAL 101, 101, 101, side-by-side, no space.

    ☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐
    ⊹─────────────⟡─────────────⊹
    ==>
    ```

2.  **Analyze the request:** The server asks for "ASCII DECIMAL 101, 101, 101, side-by-side, no space."
    ASCII decimal 101 corresponds to the character `e`. So, the string we need to send is `eee`.

3.  **Send the payload:** We can write a simple Python script to connect, receive the prompt, and send the response:

    ```python
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("candy-mountain.picoctf.net", 61433))

    def read_until(s, prompt):
        data = b""
        while prompt not in data:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        return data

    print(read_until(s, b"==> ").decode())
    s.sendall(b"eee\n")
    print(read_until(s, b"==> ").decode())
    ```

4.  **Retrieve the flag:** Running the script outputs the flag.

## Flag
`picoCTF{pr1n74813_ch4r5_15ddc7a7}`