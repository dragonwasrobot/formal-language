# finite_automaata.py

# An implementation of a (Deterministic) Finite Automata.
# Finite Automatas are usually used in Formal Language Theory to reason about
# regular languages.
#
# Author: Peter Urbak
# Version: 2012-04-26
import copy

class IllegalCharacterError(Exception):
    """This error is raised whenever a character not found in a Finite Automatas
    alphabet is trying to be used in some method context."""

    def __init__(self, character):
        self.character = character

    def __str__(self):
        return repr(self.character)

class FiniteAutomata(object):
    """A Finite Automata."""

    # --*-- Constructors --*--

    def __init__(self, states, alphabet, initial, accept, transitions):
        """Constructs a new Finite Automata.

        @param states: A set of states.
        @type states: list.

        @param alphabet: The set of symbols.
        @type alphabet: list.

        @param initial: The initial state.
        @type initial: str.

        @param accept: The set of accepting states.
        @type accept: list.

        @param transitions: A dictionary of 2-tuples (Q_old, \Sigma) mapping to
        a symbol Q_new.
        @type transitions: dict.
        """

        # input
        self.states = states
        self.alphabet = alphabet
        self.initial = initial
        self.accept = accept
        self.transitions = transitions

    # --*-- Methods --*--

    # Some of these guys may be a bit too Java'ish.

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

    def toRegExp():
        """Converts the Finite Automata to its equivalent regular
        expression. [Martin Th. 4.5]"""
        pass

    def complement():
        """Constructs a new automaton that accepts the complement of the
        language of this automaton."""
        states = copy.copy(self.states) # lists are mutable, ieeew.
        alphabet = copy.copy(self.alphabet) # lists are mutable, ieeew.
        initial = self.initial # strings are immutable, <3.
        # accept =
        states = self.states
        pass

# Old stuff

'''
    def lookupAction(self, state, symbol):
        """Returns the rule (5-tuple) governing the specified combination of
        (state, symbol).

        @param state: The current state.
        @type state: string

        @param symbol: The current symbol.
        @type symbol: string

        """

        for transition in self.transition_function:
            if transition[0] == state and transition[1] == symbol:
                return transition
        return (state, symbol, state, 'HALT', 'N')

    def run(self, tape):
        """Runs the Turing Machine on the specified input tape.

        @param tape: The input tape; a list of symbols composing the intended
                     input value for the turing machine.
        @type tape: list of strings

        """
        self.hasAccepted = False
        self.hasHalted = False

        state = self.init_state
        symbol = tape[0]
        head = 0

        while self.hasHalted == False:
            transition = self.lookupAction(state, symbol)

            state = transition[2] # update state of TM
            newSymbol = transition[3] # get symbol from transition function
            direction = transition[4] # get direction from transition function

            # Check for accept state
            if state in self.accept_states:
                self.hasAccepted = True
                self.hasHalted = True

            # Check for error state
            if newSymbol == 'HALT':
                self.hasHalted = True

            # Update Head and Tape.
            tape[head] = newSymbol # write new symbol to tape

            if direction == 'R':
                head += 1
            elif direction == 'L':
                head -= 1

            # bounds check tape
            if head < 0:
                tape.insert(0,self.blank)
            elif head >= len(tape):
                tape.append(self.blank)

            symbol = tape[head]

        return tape
'''

# end-of-finite_automata.py
