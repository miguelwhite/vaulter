from setuptools import setup

setup(name='vaulter',
      version='0.0.0',
      description='Vaulter CLI tool to interactively edit vault files',
      author='Civis Team Blackbird',
      install_requires=[
        'ansible-vault~=1.2.0',
        'Click~=7.0',
        'PyYAML~=5.3',
        'python-editor~=1.0.4'
      ],
      packages=['vaulter'],
      scripts=['bin/vaulter'],
      zip_safe=False)
