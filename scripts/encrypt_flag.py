from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
from base64 import b64encode

import hashlib
import sys

def encrypt_file(key):
    key = hashlib.sha256(key.encode('utf-8')).digest()
    nonce = get_random_bytes(12)
    plaintext = b"This flag is correct!"

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    print(b64encode(nonce + tag + ciphertext).decode())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python encrypt.py <key>")
        sys.exit(1)

    encrypt_file(sys.argv[1])
