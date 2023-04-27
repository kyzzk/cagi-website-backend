from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from env import ENCRYPT_TOKEN

import base64
import os


def generate_key(salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(ENCRYPT_TOKEN.encode()))
    return key


def encrypt(data_to_encrypt):
    salt = os.urandom(16)
    key = generate_key(salt)
    f = Fernet(key)
    _encrypted_data = f.encrypt(data_to_encrypt.encode())
    encrypted_data_with_salt = salt + _encrypted_data
    return base64.b64encode(encrypted_data_with_salt).decode()


def decrypt(encrypted_data_base64):
    encrypted_data_with_salt = base64.b64decode(encrypted_data_base64.encode())
    salt = encrypted_data_with_salt[:16]
    _encrypted_data = encrypted_data_with_salt[16:]
    key = generate_key(salt)
    f = Fernet(key)
    _decrypted_data = f.decrypt(_encrypted_data)
    return _decrypted_data.decode()
