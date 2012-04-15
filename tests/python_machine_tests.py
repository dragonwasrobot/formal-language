# python-machine_tests.py

from nose.tools import *
import python_machine

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"

# end-of-python-machine_tests.py
