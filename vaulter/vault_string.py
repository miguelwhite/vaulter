import os
import yaml
from ansible_vault import Vault

class VaultString(object):
    """Custom object for vault encrypted strings."""

    def __init__(self, value):
        """Initialize Encrypted Vault string object."""
        self.value = value

    def __str__(self):
        """String representer method."""
        return str(self.value)

    @staticmethod
    def representer(dumper, data):
        """YAML representer method for vault encrypted strings."""
        return dumper.represent_scalar(u'!vault', u'{}'.format(data))

    @staticmethod
    def constructor(loader, node):
        """YAML constructor method for vault encrypted strings."""
        value = loader.construct_scalar(node)
        return VaultString(value)

def decrypt(vault_string, vault_pass):
    """Decrypt a VaultString object with a specified Vault pass."""
    if not isinstance(vault_string, VaultString):
        raise TypeError('vault_string must be an instance of VaultString')

    vault = Vault(vault_pass)
    return vault.load(vault_string.value)

def encrypt(string, vault_pass):
    """Encrypt string with a Vault pass and return a VaultString"""
    vault = Vault(vault_pass)
    return VaultString(vault.dump_raw(string).decode('utf-8').rstrip())

def yaml_vault_tags(func):
    """Decorator for yaml representer/constructor for safe methods"""
    yaml.SafeDumper.add_representer(VaultString,
                                     VaultString.representer)
    yaml.SafeLoader.add_constructor(u'!vault',
                                     VaultString.constructor)
    return func
