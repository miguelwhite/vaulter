import pytest
import os
import yaml
import editor
from vaulter.vault_string import VaultString, yaml_vault_tags
from vaulter.commands import *

ABS_PATH = os.path.abspath(os.path.dirname(__file__))

class TestCommands:
    """Test vaulter commands."""

    @yaml_vault_tags
    def test_edit(self, mocker):
        """Test edit function."""
        mocker.patch('editor.edit', return_value=True)

        test_yaml = os.path.join(ABS_PATH, 'test.yaml')

        edit(test_yaml, 'testing')

        data = yaml.safe_load(open(test_yaml).read())

        assert isinstance(data['key1'], VaultString)

    @yaml_vault_tags
    def test_convert(self):
        """Test convert function"""
        in_file = os.path.join(ABS_PATH, 'vault.yaml')
        out_file = os.path.join(ABS_PATH, 'inline_vault.yaml')
        convert(in_file, 'test pass', out_file=out_file)

        data = yaml.safe_load(open(out_file).read())

        assert isinstance(data['foo'], VaultString)
