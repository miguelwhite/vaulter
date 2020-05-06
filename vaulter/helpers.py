import string
import random
from .vault_string import VaultString, encrypt, decrypt

def random_string(length=32):
    """Returns a random string of a given length."""
    chars = string.ascii_lowercase + string.digits
    return ''.join([random.choice(chars) for x in range(length)])

def decrypt_values(data, vault_pass):
    """Decrypts all values in a given data dictionary."""
    for key, value in data.items():
        if isinstance(value, dict):
            decrypt_values(value, vault_pass)
        else:
            if isinstance(value, VaultString):
                data[key] = decrypt(value, vault_pass)
    return data

def encrypt_values(data, vault_pass):
    """Encrypts all values in a given data dictionary."""
    for key, value in data.items():
        if isinstance(value, dict):
            encrypt_values(value, vault_pass)
        else:
            if not isinstance(value, VaultString):
                data[key] = encrypt(value, vault_pass)
    return data

def diff_and_encrypt_values(data, orig_data, vault_pass):
    """Compares data to orignal and encrypts new values only.

    Requires both datasets to be encrypted with the same vault
    password.
    """
    for key in data:
        if isinstance(data[key], dict):
            if key in orig_data.keys() and isinstance(orig_data[key], dict):
                diff_and_encrypt_values(data[key], orig_data[key], vault_pass)
            else:
                diff_and_encrypt_values(data[key], orig_data, vault_pass)
        else:
            if not isinstance(data[key], VaultString):
                # We're doing a naive check of the original encrypted
                # data dictionary. First we check if the data is dictionary.
                # We do this because we could have changed our data structure.
                # from the original
                if isinstance(orig_data, dict):
                    # If the so then we check if the key we updated is in the
                    # original dataset
                    if key in orig_data.keys():
                        # If that key is an a vaullt string instance and the
                        # decrypted value is the same, then we simply use the
                        # original value
                        if isinstance(orig_data[key], VaultString):
                            if data[key] == decrypt(orig_data[key], vault_pass):
                                data[key] = orig_data[key]
                                continue

                data[key] = encrypt(data[key], vault_pass)
    return data
