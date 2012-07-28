# finite_automata_tests.py

# Test functions for the implementation of a Finite Automata found in
# finite_automata.py.
#
# Author: Peter Urbak
# Version: 2012-07-27

from nose.tools import *
from formal_language.finite_automata import *

# -*- Helper Functions -*-

def returnFreshFA():
    """Returns the FA which accepts all strings in $\{0,1\}*$ ending in 11."""
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

# -*- Tests -*-

# * checkWellDefined *

def test_freshFAIsWellDefined():
    returnFreshFA() # constructor calls checkWellDefined()
    # Implicit assert_true test, since the check would raise an exception if
    # anything was wrong.

@raises(IllegalCharacterError)
def test_FAHasIllegalCharacterInAlphabet():
    fa = returnFreshFA()
    fa.alphabet = frozenset(['a','b','c','*','d','e'])
    checkWellDefined(fa)

@raises(IllegalArgumentError)
def test_FAHasAnAlphabetSymbolWithLengthGreaterThan1():
    fa = returnFreshFA()
    fa.alphabet = frozenset(['a','b','c','d','de','e'])
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_FAHasInitialSetToNone():
    fa = returnFreshFA()
    fa.initial = None
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_FADoesNotHaveInitialStateInStateSet():
    fa = returnFreshFA()
    fa.states = frozenset(['b','c'])
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_FADoesNotHaveAllAcceptStatesInStateSet():
    fa = returnFreshFA()
    fa.accept = frozenset(['c','d'])
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_FATransitionFunctionIsNotTotal():
    fa = returnFreshFA()
    fa.transitions  = {('a', '0') : 'a', ('a', '1') : 'b',
                       ('b', '0') : 'a', ('b', '1') : 'c'}
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_FATransitionToAStateNotFoundInStateSet():
    fa = returnFreshFA()
    fa.transitions  = {('a', '0') : 'a', ('a', '1') : 'b',
                       ('b', '0') : 'd', ('b', '1') : 'c'}
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_FATransitionReferToStateNotInStateSet():
    fa = returnFreshFA()
    fa.transitions  = {('d', '0') : 'a', ('a', '1') : 'b',
                       ('b', '0') : 'a', ('b', '1') : 'c'}
    checkWellDefined(fa)

@raises(AutomatonNotWellDefinedError)
def test_NonAlphabetSymbolAppearsInTransitions():
    fa = returnFreshFA()
    fa.transitions  = {('a', '2') : 'a', ('a', '1') : 'b',
                       ('b', '0') : 'a', ('b', '1') : 'c'}
    checkWellDefined(fa)

# * toDot *

def test_toDot():
    # print fa.toDot() # have to test this guy manually
    pass

# * getNumberOfStates *

def test_getNumberOfStates():
    fa = returnFreshFA()
    # Positive tests
    assert_equal(fa.getNumberOfStates(), 3)

# * AddTransition *

@raises(IllegalCharacterError)
def test_addTransition():
    fa = returnFreshFA()
    # Positive tests
    fa.addTransition('d', '0', 'd')
    # Exception tests
    fa.addTransition('d', '2', 'd')

# * delta *

@raises(IllegalCharacterError)
def test_delta():
    fa = returnFreshFA()
    # Positive tests
    assert_equal('c', fa.delta('b','1'))
    # Exception tests
    fa.delta('d', '2')

# * deltaStar *

@raises(IllegalCharacterError)
def test_deltaStar():
    fa = returnFreshFA()
    # Positive tests
    assert_equal('c', fa.deltaStar('a','10111'))
    # Exception tests
    fa.delta('a', '1012')

# * accepts *

def test_accepts():
    fa = returnFreshFA()
    # Postive tests
    assert_true(fa.accepts('10111'))
    # Negative tests
    assert_false(fa.accepts('10110'))

# * complement *

def test_complement():
    fa = returnFreshFA()
    # Postive tests
    faComp = complement(fa)
    assert_true(faComp.accepts('10110'))
    # Negative tests
    assert_false(faComp.accepts('10111'))

# * findReachableStates *

def test_findReachableStates():
    fa = returnFreshFA()
    # Positive tests
    reachableStates = fa.findReachableStates()
    assert_equal(reachableStates, frozenset(['a','b','c']))

    fa.states = frozenset(['a','b','c','d','e'])
    reachableStates = fa.findReachableStates()
    assert_equal(reachableStates, frozenset(['a','b','c']))

# * removeUnreachableStates *

def test_removeUnreachableStates():
    fa = returnFreshFA()
    m = removeUnreachableStates(fa)
    assert_equal(m.states, frozenset(['a','b','c']))

    fa.states = frozenset(['a','b','c','d','e'])
    fa.transitions[('d','0')] = 'e'
    fa.transitions[('e','1')] = 'a'

    originalStates = ['a','b','c']
    originalTransitions = {('c', '1') : 'c', ('a', '0') : 'a', ('a', '1') : 'b',
                           ('b', '1'): 'c', ('b', '0'): 'a', ('c', '0'): 'a'}

    m = removeUnreachableStates(fa)
    assert_true(helper_setEquality(m.states, originalStates))
    assert_equal(m.transitions, originalTransitions)

# * minimize *

def test_minimize():
    # First create the FA to minimize
    states = frozenset(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    alphabet = frozenset(['a','b'])
    initial = '0'
    accept = frozenset(['3','4','8','9'])
    transitions = {('0', 'a') : '1', ('0', 'b') : '9',
                   ('1', 'a') : '8', ('1', 'b') : '2',
                   ('2', 'a') : '3', ('2', 'b') : '2',
                   ('3', 'a') : '2', ('3', 'b') : '4',
                   ('4', 'a') : '5', ('4', 'b') : '8',
                   ('5', 'a') : '4', ('5', 'b') : '5',
                   ('6', 'a') : '7', ('6', 'b') : '5',
                   ('7', 'a') : '6', ('7', 'b') : '5',
                   ('8', 'a') : '1', ('8', 'b') : '3',
                   ('9', 'a') : '7', ('9', 'b') : '8'}

    largeFA = FiniteAutomata(states, alphabet, initial, accept, transitions)

    mStates = frozenset(['0', '9', '7', '1', '3'])
    mAlphabet = alphabet
    mInitial = initial
    mAccept = frozenset(['3','9'])
    mTransitions = {('0', 'a') : '1', ('0', 'b') : '9',
                   ('9', 'a') : '7', ('9', 'b') : '3',
                   ('7', 'a') : '7', ('7', 'b') : '1',
                   ('1', 'a') : '3', ('1', 'b') : '1',
                   ('3', 'a') : '1', ('3', 'b') : '3'}

    minimalFA = FiniteAutomata(mStates, mAlphabet, mInitial, mAccept, mTransitions)

    minimizeResult = minimize(largeFA)
    assert_true(equals(minimizeResult, minimalFA))

# * isFinite *

def test_isFinite():
    pass

# * isEmpty *

def test_isEmpty():
    fa = returnFreshFA()
    assert_false(fa.isEmpty())
    emptyFA = FiniteAutomata(fa.states, fa.alphabet, fa.initial,
                               frozenset([]), fa.transitions)
    assert_true(emptyFA.isEmpty())

# * subsetOf *

def test_subsetOf():
    pass

# * equals *

def test_equals():
    pass

# * getShortestString *

def test_getShortestString():
    pass

# * intersection *

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

    compositeFA = intersection(m1, m2)

    assert_true(compositeFA.accepts('001')) # ar->bs->br->cs (accept)
    assert_false(compositeFA.accepts('01')) # ar->bs->cr (reject)
    assert_false(compositeFA.accepts('1')) # ar->bs (reject)

# * union *

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

    compositeFA = union(m1, m2)

    assert_true(compositeFA.accepts('001')) # ar->bs->br->cs (accept)
    assert_true(compositeFA.accepts('01')) # ar->bs->cr (accept)
    assert_true(compositeFA.accepts('1')) # ar->bs (accept)
    assert_false(compositeFA.accepts('00')) # ar->bs->br (reject)

# * minus *

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

    compositeFA = minus(m1, m2)

    assert_false(compositeFA.accepts('001')) # ar->bs->br->cs (reject)
    assert_true(compositeFA.accepts('01')) # ar->bs->cr (accept)
    assert_false(compositeFA.accepts('1')) # ar->bs (reject)
    assert_false(compositeFA.accepts('00')) # ar->bs->br (reject)

# * toNondeterministicFiniteAutomata *

# * toRegularExpression *

# end-of-finite_automata_tests.py
