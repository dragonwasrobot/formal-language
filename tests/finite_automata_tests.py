# finite_automata_tests.py

from nose.tools import *
from formal_language.finite_automata import *

# Helper functions

def returnFreshFA():
    """Returns the FA which accepts all strings in {0,1}* ending in 11."""
    states = frozenset(['a', 'b', 'c'])
    alphabet = frozenset(['0','1'])
    initial = 'a'
    accept = frozenset(['c'])
    transitions = {('a', '0') : 'a', ('a', '1') : 'b',
                   ('b', '0') : 'a', ('b', '1') : 'c',
                   ('c', '0') : 'a', ('c', '1') : 'c'}

    fa = FiniteAutomata(states, alphabet, initial, accept, transitions)
    return fa

def helper_setEquality(Xs, Ys):
    """Slow comparison, could probably be done faster with hashing."""
    if len(Xs) != len(Ys):
        return False

    for x in Xs:
        if x not in Ys:
            return False

    return True

# Tests

@raises(IllegalCharacterError)
def test_alphabet1():
    fa = returnFreshFA()

    # Positive
    assert_true(fa.checkAlphabet())
    # Exception
    fa.alphabet = frozenset(['a','b','c','*','d','e'])
    fa.checkAlphabet()

@raises(IllegalArgumentError)
def test_alphabet2():
    fa = returnFreshFA()
    # Exception
    fa.alphabet = frozenset(['a','b','c','d','de','e'])
    fa.checkAlphabet()

def test_toDot():
    # print fa.toDot() # have to test this guy manually
    pass

def test_checkWellDefined():
    # Positive Tests
    # assertTrue(fa.checkWellDefined())
    # Negative Tests
    pass

def test_numberOfStates():
    fa = returnFreshFA()
    # Positive tests
    assert_equal(fa.getNumberOfStates(), 3)

@raises(IllegalCharacterError)
def test_addTransitions():
    fa = returnFreshFA()
    # Positive tests
    fa.addTransition('d', '0', 'd')
    # Exception tests
    fa.addTransition('d', '2', 'd')

@raises(IllegalCharacterError)
def test_delta():
    fa = returnFreshFA()
    # Positive tests
    assert_equal('c', fa.delta('b','1'))
    # Exception tests
    fa.delta('d', '2')

@raises(IllegalCharacterError)
def test_deltaStar():
    fa = returnFreshFA()
    # Positive tests
    assert_equal('c', fa.deltaStar('a','10111'))
    # Exception tests
    fa.delta('a', '1012')

def test_accepts():
    fa = returnFreshFA()
    # Postive tests
    assert_true(fa.accepts('10111'))
    # Negative tests
    assert_false(fa.accepts('10110'))

def test_complement():
    fa = returnFreshFA()
    # Postive tests
    faComp = fa.complement()
    assert_true(faComp.accepts('10110'))
    # Negative tests
    assert_false(faComp.accepts('10111'))

def test_findReachableStates():
    fa = returnFreshFA()
    # Positive tests
    reachableStates = fa.findReachableStates()
    assert_equal(reachableStates, frozenset(['a','b','c']))

    fa.states = frozenset(['a','b','c','d','e'])
    reachableStates = fa.findReachableStates()
    assert_equal(reachableStates, frozenset(['a','b','c']))

def test_removeUnreachableStates():
    fa = returnFreshFA()
    m = fa.removeUnreachableStates()
    assert_equal(m.states, frozenset(['a','b','c']))

    fa.states = frozenset(['a','b','c','d','e'])
    fa.transitions[('d','0')] = 'e'
    fa.transitions[('e','1')] = 'a'

    originalStates = ['a','b','c']
    originalTransitions = {('c', '1') : 'c', ('a', '0') : 'a', ('a', '1') : 'b',
                           ('b', '1'): 'c', ('b', '0'): 'a', ('c', '0'): 'a'}

    m = fa.removeUnreachableStates()
    assert_true(helper_setEquality(m.states, originalStates))
    assert_equal(m.transitions, originalTransitions)

def test_isEmpty():
    fa = returnFreshFA()
    assert_false(fa.isEmpty())
    emptyFA = FiniteAutomata(fa.states, fa.alphabet, fa.initial,
                               frozenset(['d']), fa.transitions)
    assert_true(emptyFA.isEmpty())

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
