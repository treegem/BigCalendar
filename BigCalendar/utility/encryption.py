import hashlib


def encrypt_sha256(string: str):
    utf_encoded = string.encode('utf-8')
    return hashlib.sha3_256(utf_encoded).hexdigest()
