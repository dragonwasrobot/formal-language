# python-machine.py

# A Turing Machine written in Python.
#
# Author: Peter Urbak
# Version: 2012-04-15

# Special blank character: #
# Alphabet: a list of symbols
# Tape: an infinite List
# Head: a tuple (index, symbol)
# Table (transition function): 5 tuples (q_i a_j -> q_i1 a_j1 d_k)
# - Either erase or write a symbol (a_j -> a_j1) then
# - Move the head in direction: d_k (L,R,N), then
# - Assume the same or a new state as prescribed (go to state q_i1)
# if no combination of symbol and state in table -> halt or require all entries
# to be filled prior
# State Register: stores the state: finitely many and a special start state

# Formal definition
# 7-Tuple $M = \tuple{Q, Gamma, b, Sigma, delta, q_0, F}
# - Q: a finite non-empty set of states
# - Gamma: finite non-empty set of tape alphabet/symbols
# - b \in Gamma: the blank symbol
# - Sigma \subset Gamma\\\{b\}: the set of input symbols
# - q_0 \in Q: the initial state
# - F \subset Q: the set of final/accepting states
# - delta: Q\F x Gamma -> Q\F x Gamma x {L,R}: transition function

# Busy Beaver:
# Q = {A, B, C, HALT}
# Gamma = {0,1}
# b = 0 = "blank"
# Sigma = {1}
# delta = (see state table)
# q_0 = A
# F = the one element set of final states {HALT}

class TuringMachine(object):
    """A Turing Machine

    This class represents a Turing Machine; Informally, a Turing
    Machine manipulates symbols of an infinite tape according to a table of
    rules.

    """

    def __init__(self, states, alphabet, blank, transition_function, init_state,
                 accept_states, tape):
        """Initializes a Turing Machine.
        @param states: A set of states; a list of strings.

        @param alphabet: The set of symbols; a list of character symbols.

        @param blank: The blank symbol; a character symbol, usually '#'.

        @param transition_function: The transition function; a list of 5-tuples:
                                    (q_i, a_i, q_{i+1}, a_{i+1}, d_k), where 'q'
                                    denotes a state, 'a' a symbol and 'd' a
                                    direction found in the set [L,R,N].

        @param init_state: The initial state; A string specifying the initial
                           state of the machine.

        @param accept_states: The set of accepting states; a list of strings
                              specifying which states are the accepting ones.

        @param tape: The input tape; a list of symbols composing the intended
                     input value for the turing machine.
        """

        self.states = states
        self.alphabet = alphabet
        self.blank = blank
        self.transition_function = transition_function
        self.init_state = init_state
        self.accept_states = accept_states
        self.tape = tape
        self.head = 0

    def lookupAction(state, symbol):
        pass

# end-of-python-machine.py
