import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.fernet import Fernet
from . import utils as Utils
from pathlib import Path


def generate_secret_key():
    secret_file = Path('secretkey.key')
    if(secret_file.exists()==False):
        key = Fernet.generate_key()
        print(f"Generated Key: {key.decode()}")

        # string the key in a file
        with open('secretkey.key', 'wb') as filekey:
            filekey.write(key)
        

def encrypt_data(data):
    generate_secret_key()
    with open('secretkey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)
    secret_value = fernet.encrypt(data.encode())
    print(secret_value)
    return secret_value


def decrypt_data(data):
    secret_key = generate_secret_key()
    fernet = Fernet(secret_key)
    secret_value = fernet.decrypt(data)
    return secret_value

