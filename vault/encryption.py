import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Derive key from password + salt
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def encrypt_file(password: str, file_data: bytes):
    salt = os.urandom(16)
    iv = os.urandom(12)

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    encrypted_data = aesgcm.encrypt(iv, file_data, None)

    return encrypted_data, salt, iv


def decrypt_file(password: str, salt: bytes, iv: bytes, encrypted_data: bytes):
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(iv, encrypted_data, None)
