import pytest
import os
import yaml
from copy import deepcopy
from vaulter.vault_string import VaultString, encrypt
from vaulter.helpers import *

ABS_PATH = os.path.abspath(os.path.dirname(__file__))

class TestHelpers:
    """Test vaulter helpers."""

    def test_random_string(self):
        """Test random_string function."""
        assert random_string() != random_string()
        assert len(random_string(16)) == 16

    def test_decrypt_values(self):
        """Test decrypt_values function."""
        enc_string = encrypt('test', 'test pass')
        data = {'foo': enc_string, 'bar': {'bar1': enc_string }}

        assert decrypt_values(data, 'test pass') == \
            {'foo': 'test', 'bar': {'bar1': 'test'}}

    def test_encrypt_values(self):
        """Test encrypt_values function."""
        data = {'foo': 'test', 'bar': {'bar1': 'test'}}
        enc_data = encrypt_values(data, 'test pass')

        assert isinstance(enc_data['foo'], VaultString)
        assert isinstance(enc_data['bar']['bar1'], VaultString)

    def test_diff_and_encrypt_values(self):
        """Test diff_and_encrypt_values function."""
        data = {'foo': 'test',
                'bar': {'bar1': 'test'},
                'foobar': 'test'}

        # encrypt a copy of the orignal data set
        enc_data_orig = encrypt_values(deepcopy(data), 'test pass')

        # edit the data set with a new value
        data['foobar'] = {'foobar1': 'new value'}

        # The new encrypted dataset should only have
        # the new value updated
        enc_data_new = diff_and_encrypt_values(data, enc_data_orig, 'test pass')

        assert enc_data_new['foo'] == enc_data_orig['foo']
        assert enc_data_new['bar'] == enc_data_orig['bar']
        assert enc_data_new['foobar'] != enc_data_orig['foobar']
