# setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description' : 'A Turing Machine written in Python',
    'author' : 'Peter Urbak',
    'url' : 'https://github.com/dragonwasrobot/python-machine',
    'download_url' : 'https://github.com/dragonwasrobot/python-machine',
    'author_email' : 'peter@dragonwasrobot.com',
    'version' : '0.1',
    'install_requires' : ['nose'],
    'packages' : ['python-machine'],
    'scripts' : [],
    'name' : 'python-machine'
    }

setup(**config)

# end-of-setup.py
