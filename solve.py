import base64
import binascii
import urllib.parse
import codecs

def decode_message(filename="message.txt"):
    with open(filename, "r") as f:
        msg = f.read().strip()

    # Step 1: Base64 decode
    msg = base64.b64decode(msg)

    # Step 2: Hex decode
    msg = binascii.unhexlify(msg).decode('utf-8')

    # Step 3: URL decode
    msg = urllib.parse.unquote(msg)

    # Step 4: ROT13 decode
    flag = codecs.decode(msg, 'rot_13')

    return flag

if __name__ == "__main__":
    flag = decode_message()
    print("Flag:", flag)
