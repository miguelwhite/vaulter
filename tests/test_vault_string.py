import pytest
import os
import yaml
from vaulter.vault_string import *

ABS_PATH = os.path.abspath(os.path.dirname(__file__))

class TestVaultString:
    """Test vaulter vault_string."""

    def test_initialization(self):
        """Test initialization of a VaultString object"""
        test_vault_string = VaultString('testing')

        assert isinstance(test_vault_string, VaultString)

    def test_encrypt(self):
        """Test encrypt and decrypt functions."""
        encrypted_string = encrypt('test string', 'test password')

        assert isinstance(encrypted_string, VaultString)
        assert str(encrypted_string).startswith('$ANSIBLE_VAULT')

    def test_decrypt(self):
        encrypted_string = encrypt('test string', 'test password')

        assert decrypt(encrypted_string, 'test password') == \
            'test string'
        with pytest.raises(TypeError):
            decrypt('not a vault string', 'test password')

    @yaml_vault_tags
    def test_yaml_safe(self):
        """Test yaml safe load and safe dump with decorator"""
        yaml_file = open(os.path.join(ABS_PATH, 'test.yaml')).read()

        data = yaml.safe_load(yaml_file)

        # yaml !safe load should not know how to parse vault tag
        with pytest.raises(yaml.constructor.ConstructorError):
            yaml.load(yaml_file, Loader=yaml.Loader)

        assert isinstance(data['key1'], VaultString)

        assert yaml.safe_dump({'foo': VaultString('bar')}) == \
            "foo: !vault 'bar'\n"

        # yaml !safe dump should not dump out correct yaml
        assert yaml.dump({'foo': VaultString('bar')}) != \
            "foo: !vault 'bar'\n"
