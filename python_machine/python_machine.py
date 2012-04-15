# python_machine.py

# A Turing Machine written in Python.
#
# Author: Peter Urbak
# Version: 2012-04-15

class TuringMachine(object):
    """A Turing Machine

    This class represents a Turing Machine; Informally, a Turing
    Machine manipulates symbols of an infinite tape according to a table of
    rules.

    """

    # --*-- Properties --*--

    hasAccepted = False
    hasHalted = False

    # --*-- Constructors --*--

    def __init__(self, states, alphabet, blank, transition_function, init_state,
                 accept_states):
        """Initializes a Turing Machine.

        @param states: A set of states.
        @type states: list of strings.

        @param alphabet: The set of symbols.
        @type alphabet: list of strings.

        @param blank: The blank symbol, usually a character like '#'.
        @type blank: string.

        @param transition_function: The transition function; a list of 5-tuples:
                                    (q_i, a_i, q_{i+1}, a_{i+1}, d_k), where 'q'
                                    denotes a state, 'a' a symbol and 'd' a
                                    direction found in the set [L,R,N].
        @type transition_function: list of tuples.

        @param init_state: The initial state; A string specifying the initial
                           state of the machine.
        @type init_state: string.

        @param accept_states: The set of accepting states; a list of strings
                              specifying which states are the accepting ones.
        @type list of strings.

        """

        # input
        self.states = states
        self.alphabet = alphabet
        self.blank = blank
        self.transition_function = transition_function
        self.init_state = init_state
        self.accept_states = accept_states

    # --*-- Methods --*--

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

# end-of-python_machine.py
