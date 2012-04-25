# setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description' : 'A Package containing constructs used in formal language
    theory.',
    'author' : 'Peter Urbak',
    'url' : 'https://github.com/dragonwasrobot/formal-language',
    'download_url' : 'https://github.com/dragonwasrobot/formal-language',
    'author_email' : 'peter@dragonwasrobot.com',
    'version' : '0.2',
    'install_requires' : ['nose'],
    'packages' : ['formal-language'],
    'scripts' : [],
    'name' : 'formal-language'
    }

setup(**config)

# end-of-setup.py
