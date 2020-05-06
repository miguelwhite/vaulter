import os
import yaml
import editor
from copy import deepcopy
from ansible_vault import Vault
from .helpers import (random_string,
                      encrypt_values,
                      decrypt_values,
                      diff_and_encrypt_values)
from .vault_string import yaml_vault_tags
import sys

@yaml_vault_tags
def edit(yaml_file, vault_pass):
    tmp_file_name = '.{}.{}.tmp'.format(random_string(),
                                        os.path.basename(yaml_file))
    original_data = yaml.safe_load(open(yaml_file).read())

    unencrypted_data = decrypt_values(deepcopy(original_data),
                                       vault_pass)

    with open(tmp_file_name, 'w') as tmp_file:
        header = ('# NOTE: This is a vault encrypted yaml file. Every value\n'
                  '# in this file will be encrypted regardless if it wasn\'t\n'
                  '# encrypted before. If you do not wish to encrypt a value,\n'
                  '# you should move it to a non vault encrypted file.\n'
                  '---\n')
        tmp_file.write(header)
        yaml.safe_dump(unencrypted_data,
                       tmp_file,
                       default_flow_style=False)
        tmp_file.close()

    try:
        editor.edit(filename=tmp_file_name, use_tty=True)
        encrypted_data = diff_and_encrypt_values(yaml.safe_load(open(tmp_file_name)),
                                           original_data,
                                           vault_pass)
        yaml.safe_dump(encrypted_data,
                       open(yaml_file, 'w'),
                       default_style='|',
                       default_flow_style=False)
    finally:
        if os.path.exists(tmp_file_name):
            os.remove(tmp_file_name)

@yaml_vault_tags
def convert(yaml_file, vault_pass, out_file=None):
    if not out_file:
        out_file = yaml_file
    vault = Vault(vault_pass)
    unencrypted_data = vault.load(open(yaml_file).read())
    encrypted_data = encrypt_values(unencrypted_data,
                                    vault_pass)

    yaml.safe_dump(encrypted_data,
                   open(out_file, 'w'),
                   default_style='|',
                   default_flow_style=False)
