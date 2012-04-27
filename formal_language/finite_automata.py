# finite_automaata.py

# An implementation of a (Deterministic) Finite Automata.
# Finite Automatas are usually used in Formal Language Theory to reason about
# regular languages.
#
# Author: Peter Urbak
# Version: 2012-04-26
import copy

# --*-- The Finite Automata --*--

class FiniteAutomata(object):
    """A Finite Automata."""

    # --*-- Constructors --*--

    def __init__(self, states, alphabet, initial, accept, transitions):
        """Constructs a new Finite Automata.

        @param states: A set of states, 'Q'.
        @type states: frozenset.

        @param alphabet: The set of symbols, '\Sigma'.
        @type alphabet: frozenset.

        @param initial: The initial state, 'q_0'.
        @type initial: str.

        @param accept: The set of accepting states, 'A'.
        @type accept: frozenset.

        @param transitions: A dictionary of 2-tuples '(Q_old, \Sigma)' mapping to
        a string symbol 'Q_new'.
        @type transitions: dict.
        """

        # input
        self.states = states
        self.alphabet = alphabet
        self.initial = initial
        self.accept = accept
        self.transitions = transitions

    # --*-- Methods --*--

    def toDot(self):
        """Produces a Graphviz Dot representation of this automaton."""
        # TODO
        pass

    def checkWellDefined(self):
        """Checks whether this automaton has been correctly defined, otherwise
        it throws one of a number of Exceptions depending on what violates the
        definition."""
        # TODO
        pass

    def getNumberOfStates(self):
        """Returns the number of states of the Finite Automata."""
        return len(self.states)

    def addTransition(self, q, c, p):
        """Adds a transition to the transition function."""
        if c not in self.alphabet:
            raise IllegalCharacterError(c)

        self.transitions[(q,c)] = p

    def delta(self, q, c):
        """Looks up the transition in the transition function."""

        if c not in self.alphabet:
            raise IllegalCharacterError(c)

        return self.transitions[(q,c)]

    def deltaStar(self, q, s):
        """Runs the given string on the Finite Automata and returns the state it
        ends up in."""
        for c in s:
            if c not in self.alphabet:
                raise IllegalCharacterError(c)
            q = self.delta(q, c)

        return q

    def accepts(self, s):
        """Runs the given string on the Finite Automata and returns true if the
        string is accepted by the automata, false otherwise."""
        return self.deltaStar(self.initial, s) in self.accept

    def toRegExp(self):
        """Converts the Finite Automata to its equivalent regular
        expression. [Martin Th. 4.5]"""
        # TODO
        pass

    def complement(self):
        """Constructs a new automaton that accepts the complement of the
        language of this automaton."""
        # All properties have an immutable type so no need to use copy.
        states = self.states
        alphabet = self.alphabet
        initial = self.initial
        accept = self.states.difference(self.accept)
        transitions = copy.copy(self.transitions)
        return FiniteAutomata(states, alphabet, initial, accept, transitions)

    def findReachableStates(self):
        """Finds the set of states that are reachable from the initial state."""
        # TODO
        pass

    def removeUnreachableStates(self):
        """Returns a new automaton with the same language as this automaton
        but without unreachable states. [Martin Exercise 3.29]"""
        # TODO
        pass

    def minimize(self):
        """Returns a new minimal automaton with the same language as this
        automaton. [Martin, Sec 5.2]"""
        # TODO
        pass

    def isFinite(self):
        """Returns true if the language of this automaton is finite. [Martin,
        Sec 5.4]"""
        # TODO
        pass

    def isEmpty(self):
        """Returns true if the language of the automaton is empty. [Martin,
        Sec. 5.4]"""
        # TODO
        pass

    def subsetOf(self, fa):
        """Returns true if the language of this automaton is a subset of the
        language of the given automaton. [Martin, Sec. 5.4]"""
        # TODO
        pass

    def equals(self, fa):
        """Returns true if the language of this automaton is equal to the
        language of the given automaton. [Martin, Sec. 5.4]"""
        # TODO
        pass

    def getShortestString(self):
        """Returns the shortest string that is accepted by this
        automaton. Returns None if the language is empty."""
        # TODO
        pass

    def intersection(self, fa):
        """Returns a new automaton whose language is the intersection of the
        language of this automaton and the language of the given
        automaton. [Martin, Th. 3.4]"""
        # TODO
        pass

    def union(self, fa):
        """Returns a new automaton whose language is the union of the
        language of this automaton and the language of the given
        automaton. [Martin, Th. 3.4]"""
        # TODO
        pass

    def minus(self, fa):
        """Returns a new automaton whose language is equal to the language of
        this automaton minus the language of the given automaton. [Martin,
        Th. 3.4]"""
        # TODO
        pass

# --*-- Exceptions --*--

class IllegalCharacterError(Exception):
    """This error is raised whenever a character not found in a Finite Automatas
    alphabet is trying to be used in some method context."""

    def __init__(self, character):
        """Initializes an IllegalCharacterError object."""
        self.character = character

    def __str__(self):
        """Returns a description of the error which occured."""
        return repr(self.character)

class AutomatonNotWellDefinedException(Exception):
    """This error is raised whenever a automaton has not been correctly
    constructed according to its definition."""

    def __init__(self, message):
        """Initializes an IllegalCharacterError object."""
        self.message = message

    def __str__(self):
        """Returns the error message of the Exception."""
        return repr(self.message)

# end-of-finite_automata.py
