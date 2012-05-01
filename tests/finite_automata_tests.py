# finite_automata_tests.py

from nose.tools import *
from formal_language.finite_automata import *

# The FA which accepts all strings in {0,1}* ending in 11.
states = frozenset(['a', 'b', 'c'])
alphabet = frozenset(['0','1'])
initial = 'a'
accept = frozenset(['c'])
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

def test_complement():
    # Postive test
    faComp = fa.complement()
    assert_true(faComp.accepts('10110'))
    # Negative test
    assert_false(faComp.accepts('10111'))

def test_intersection():
    statesM1 = frozenset(['a', 'b', 'c'])
    alphabet = frozenset(['0','1'])
    initialM1 = 'a'
    acceptM1 = frozenset(['c'])
    transitionsM1 = { ('a', '0') : 'b', ('a', '1') : 'a',
                      ('b', '0') : 'b', ('b', '1') : 'c',
                      ('c', '0') : 'b', ('c', '1') : 'a' }
    m1 = FiniteAutomata(statesM1, alphabet, initialM1, acceptM1, transitionsM1)

    statesM2 = frozenset(['r','s'])
    initialM2 = 'r'
    acceptM2 = frozenset(['s'])
    transitionsM2 = {('r', '0') : 's', ('r', '1') : 's',
                     ('s', '0') : 'r', ('s', '1') : 'r'}

    m2 = FiniteAutomata(statesM2, alphabet, initialM2, acceptM2, transitionsM2)

    compositeFA = m1.intersection(m2)

    assert_true(compositeFA.accepts('001')) # ar->bs->br->cs (accept)
    assert_false(compositeFA.accepts('01')) # ar->bs->cr (reject)
    assert_false(compositeFA.accepts('1')) # ar->bs (reject)

def test_union():
    statesM1 = frozenset(['a', 'b', 'c'])
    alphabet = frozenset(['0','1'])
    initialM1 = 'a'
    acceptM1 = frozenset(['c'])
    transitionsM1 = { ('a', '0') : 'b', ('a', '1') : 'a',
                      ('b', '0') : 'b', ('b', '1') : 'c',
                      ('c', '0') : 'b', ('c', '1') : 'a' }
    m1 = FiniteAutomata(statesM1, alphabet, initialM1, acceptM1, transitionsM1)

    statesM2 = frozenset(['r','s'])
    initialM2 = 'r'
    acceptM2 = frozenset(['s'])
    transitionsM2 = {('r', '0') : 's', ('r', '1') : 's',
                     ('s', '0') : 'r', ('s', '1') : 'r'}

    m2 = FiniteAutomata(statesM2, alphabet, initialM2, acceptM2, transitionsM2)

    compositeFA = m1.union(m2)

    assert_true(compositeFA.accepts('001')) # ar->bs->br->cs (accept)
    assert_true(compositeFA.accepts('01')) # ar->bs->cr (accept)
    assert_true(compositeFA.accepts('1')) # ar->bs (accept)
    assert_false(compositeFA.accepts('00')) # ar->bs->br (reject)

def test_minus():
    statesM1 = frozenset(['a', 'b', 'c'])
    alphabet = frozenset(['0','1'])
    initialM1 = 'a'
    acceptM1 = frozenset(['c'])
    transitionsM1 = { ('a', '0') : 'b', ('a', '1') : 'a',
                      ('b', '0') : 'b', ('b', '1') : 'c',
                      ('c', '0') : 'b', ('c', '1') : 'a' }
    m1 = FiniteAutomata(statesM1, alphabet, initialM1, acceptM1, transitionsM1)

    statesM2 = frozenset(['r','s'])
    initialM2 = 'r'
    acceptM2 = frozenset(['s'])
    transitionsM2 = {('r', '0') : 's', ('r', '1') : 's',
                     ('s', '0') : 'r', ('s', '1') : 'r'}

    m2 = FiniteAutomata(statesM2, alphabet, initialM2, acceptM2, transitionsM2)

    compositeFA = m1.minus(m2)

    assert_false(compositeFA.accepts('001')) # ar->bs->br->cs (reject)
    assert_true(compositeFA.accepts('01')) # ar->bs->cr (accept)
    assert_false(compositeFA.accepts('1')) # ar->bs (reject)
    assert_false(compositeFA.accepts('00')) # ar->bs->br (reject)


# end-of-turing_machine_tests.py
