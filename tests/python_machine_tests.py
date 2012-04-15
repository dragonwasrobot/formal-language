# python-machine_tests.py

from nose.tools import *
from python_machine.python_machine import *

states = ['A','F']
alphabet = ['1', '#']
blank = '#'
transition_function = [('A','1','A','1','R'),
                       ('A','#','F','1','N')]
init_state = 'A'
accept_state = 'F'

tm = TuringMachine(states, alphabet, blank, transition_function, init_state,
                   accept_state)

def test_lookupAction():
    assert_equal(tm.lookupAction('A', '1'), ('A','1','A','1','R'))
    assert_equal(tm.lookupAction('A', '#'), ('A','#','F','1','N'))
    assert_equal(tm.lookupAction('B', '#'), ('B', '#', 'B', 'HALT', 'N'))

def test_run():
    assert_equal(tm.run(['1']), ['1','1'])
    assert_equal(tm.run(['1','1','1']), ['1','1','1','1'])
    assert_equal(tm.run(['2']), ['HALT'])

# end-of-python-machine_tests.py
