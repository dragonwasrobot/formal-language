# finite_automata_tests.py

from nose.tools import *
from formal_language.finite_automata import *

# The FA which accepts all strings in {0,1}* ending in 11.
states = ['a', 'b', 'c']
alphabet = ['0','1']
initial = 'a'
accept = ['c']
transitions = {('a', '0') : 'a', ('a', '1') : 'b',
               ('b', '0') : 'a', ('b', '1') : 'c',
               ('c', '0') : 'a', ('c', '1') : 'c'}

fa = FiniteAutomata(states, alphabet, initial, accept, transitions)

# A faulty

def test_numberOfStates():
    # Positive test
    assert_equal(fa.getNumberOfStates(), 3)

@raises(IllegalCharacterError)
def test_addTransitions():
    # Positive test
    fa.addTransition('d', '0', 'd')
    # Exception test
    fa.addTransition('d', '2', 'd')

@raises(IllegalCharacterError)
def test_delta():
    # Positive test
    assert_equal('c', fa.delta('b','1'))
    # Exception test
    fa.delta('d', '2')

@raises(IllegalCharacterError)
def test_deltaStar():
    # Positive test
    assert_equal('c', fa.deltaStar('a','10111'))
    # Exception test
    fa.delta('a', '1012')

def test_accepts():
    # Postive test
    assert_true(fa.accepts('10111'))
    # Negative test
    assert_false(fa.accepts('10110'))

def test_correctness():
    pass


# end-of-turing_machine_tests.py
