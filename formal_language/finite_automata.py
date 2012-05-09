# finite_automata.py

# An implementation of a (Deterministic) Finite Automata.
# Finite Automatas are used in Formal Language Theory to reason about
# regular languages.
#
# Author: Peter Urbak
# Version: 2012-05-09
import copy
import subprocess
from exceptions import *
from nondeterministic_finite_automata import *

# --*-- Finite Automata --*--

class FiniteAutomata(object):
    """A Finite Automata.

    Definition 1: A Finite Automaton
    A finite automaton (FA) is a 5-tuple (Q, \Sigma, q_0, A, \delta), where

    Q is a finite set of states;
    \Sigma is a finite input alphabet;
    q_0 \in Q is the initial state;
    A \subseteq Q is the set of accepting states;
    \delta: Q \times \Sigma \to Q is the transition function.

    For any element in q of Q and any symbol \sigma \in Sigma, we interpret
    \delta(q, \sigma) as the state to which the FA moves, if it is in state q
    and receives the input \sigma.
    """

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

        self.checkWellDefined()

    # --*-- Methods --*--

    def checkWellDefined(self):
        """Checks that this automaton is well-defined. In particular, this
        method checks that the transition function is total."""
        illegalSymbols = frozenset(['#','%','+','*','(',')'])

        if len(illegalSymbols & self.alphabet) > 0:
            raise IllegalCharacterError("'#', '%', '+', '*', '(' and ')'"  \
                                            + "are not allowed in the alphabet")

        if len(max(self.alphabet, key=len)) > 1:
            raise IllegalArgumentError("Alphabet symbols must have length" \
                                           + "of exactly 1")

        if self.states is None or self.alphabet is None \
                or self.initial is None or self.accept is None \
                or self.transitions is None:
            raise AutomatonNotWellDefinedError("An argument was set to None.")

        if self.initial not in self.states:
            raise AutomatonNotWellDefinedError("The initial state is not in " \
                                                   + "the state set.")

        if len(self.accept & self.states) < len(self.accept):
            raise AutomatonNotWellDefinedError("Not all accept states are in " \
                                                   + "the state set.")

        for state in self.states:
            for symbol in self.alphabet:
                try:
                    toState = self.delta(state, symbol)
                    if toState not in self.states:
                        raise AutomatonNotWellDefinedError(\
                            "There is a transition to a state which cannot be "\
                                + "found in the state set.")
                except KeyError:
                    raise AutomatonNotWellDefinedError("Transition function " \
                                                           + "is not total.")

        for stateSymbolPair, resultState in self.transitions.items():
            if stateSymbolPair[0] not in self.states:
                raise AutomatonNotWellDefinedError(\
                    "Transitions refer to a state not in state set.")
            if stateSymbolPair[1] not in self.alphabet:
                raise AutomatonNotWellDefinedError(\
                    "Non-alphabet symbol appears in transitions.")

        return True

    def toDot(self, outputFile = "./fa.gv"):
        """Creates a Graphviz Dot file (.gv) at the given path and also tries to
        create a pdf version of the finite automata at the same time."""

        outputString = "digraph finite_automaton {\n\trankdir = LR;\n"

        outputString += "\tstart [shape = point, color = white, " \
            + "fontcolor = white];\n"

        for state in self.states:
            if state in self.accept:
                outputString += "\t" + state + " [shape = doublecircle, " \
                + "color = black, fontcolor = black, label = \"" + state \
                + "\"];\n"
            else:
                outputString += "\t" + state + " [shape = circle, " \
                + "color = black, fontcolor = black, label = \"" + state \
                + "\"];\n"

        outputString += "\tstart -> " + self.initial + ";\n"
        for state in self.states:
            for character in self.alphabet:
                toState = self.delta(state, character)
                outputString += "\t" + state + " -> " + toState \
                    + " [ label = \"" + character + "\" ];\n"

        outputString += "}\n"

        # Create output file and convert to pdf using Graphviz.
        f = open(outputFile, 'w')
        f.write(outputString)
        f.close()

        pdfFile = outputFile.rstrip('.gv') + '.pdf'
        subprocess.call(["dot", "-Tpdf", outputFile, "-o", pdfFile])

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
        ends up in.

        Definition 2: The Extended Transition Function \delta*

        Let M = (Q, \Sigma, q_0, A, \deta) be a finite automaton. We define the
        extended transition function

        \delta* : Q \times \Sigma* \to Q

        as follows:

        1. For every q \in Q, \delta*(q, \Lambda) = q
        2. For every q \in Q, every y \in \Sigma*, and every \sigma \in \Sigma,

        \delta*(q, y\sigma) = \delta(\delta*(q,y),\sigma).

        @param q: a state
        @type q: str

        @param s: a string of alphabet symbols
        @type s: str

        """
        for c in s:
            if c not in self.alphabet:
                raise IllegalCharacterError(c)
            q = self.delta(q, c)

        return q

    def accepts(self, s):
        """Runs the given string on the Finite Automata and returns true if the
        string is accepted by the automata, false otherwise.

        Definition 3: Acceptance by a Finite Automaton

        Let M = (Q, \Sigma, q_0, A, \delta) be an FA, and let x \in \Sigma*. The
        string x is accepted by M if

        \delta*(q_0,x) \in A

        and is rejected by M otherwise.

        The language accepted by M is the set

        L(M) = {x \in \Sigma* | x is accepted by M}

        if L is a language over \Sigma, L is accepted by M if and only if
        L = L(M).

        @param s: a string of alphabet symbols
        @type s: str
        """
        return self.deltaStar(self.initial, s) in self.accept

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

        reachable = []
        pending = []
        pending.append(self.initial)

        while len(pending) > 0:
            q = pending.pop()
            reachable.append(q)

            for c in self.alphabet:
                p = self.delta(q, c)
                if p not in reachable:
                    pending.append(p)

        return frozenset(reachable)

    def removeUnreachableStates(self):
        """Returns a new automaton with the same language as this automaton
        but without unreachable states."""
        reachable = self.findReachableStates()

        states = self.states - (self.states - reachable)
        alphabet = self.alphabet
        initial = self.initial
        accept = self.accept - (self.accept - reachable)
        transitions = {}

        for stateSymbolPair, resultState in self.transitions.items():
            if stateSymbolPair[0] in states:
                transitions[stateSymbolPair] = resultState

        return FiniteAutomata(states, alphabet, initial, accept, transitions)

    def minimize(self):
        """Constructs a new minimal automaton with the same language as this
        automaton."""
        fa = self.removeUnreachableStates()
        marks = set([])
        stateList = fa.states
        # todo

    def isFinite(self):
        """Returns true if the language of this automaton is finite."""
        # The language is finite iff there is a reachable loop with a path to an
        # accept state.
        live = self._findLiveStates()
        return not self._containsLoop(self.initial, live, set([]))

    def _findLiveStates(self, s):
        """Finds the set of states among 's' that can reach an accept state.

        @param s: a set of states
        @type s: set
        """

        back = {} # p in back[q] iff delta(p,c) = q for some c
        for p in s:
            back[p] = set([])

        for p in s:
            for symbol in self.alphabet:
                q = self.delta(q, symbol)
                if q in s:
                    back[q].add(p)

        live = set(self.accept)
        pending = set(self.accept)
        while len(pending) > 0:
            q = pending.__iter__().next()
            pending.remove(q)
            for p in back[q]:
                if p not in live:
                    live.add(p)
                    pending.add(p)

        return live

    def _containsLoop(self, p, s, path):
        """Check whether there is a loop in the set 's' reachable from the state
        'p' through the states in path.

        @param p: a state
        @type p: str

        @param s: a set of states
        @type s: set

        @param path: a set of states
        @type path: set
        """

        path.add(p)
        for symbol in self.alphabet:
            q = self.delta(p, symbol)
            if q in s and (q in path or self._containsLoop(self, q, s, path)):
                return True

        path.remove(p)
        return False

    def isEmpty(self):
        """Returns true if the language of the automaton is empty."""
        # Check if there exists a state in 'accept' that is also reachable.
        return len(self.findReachableStates() & self.accept) == 0

    def subsetOf(self, fa):
        """Returns true if the language of this automaton is a subset of the
        language of the given automaton."""
        # TODO
        return False

    def equals(self, fa):
        """Checks whethe the language of this automaton is equal to the
        language of the given automaton."""
        if not isinstance(fa, FiniteAutomata):
            return False
        return self.subsetOf(fa) and fa.subsetOf(self)

    def getShortestString(self):
        """Returns the shortest string that is accepted by this
        automaton. Returns None if the language is empty."""
        # TODO Shortest path to accept state.
        pass

    def intersection(self, fa):
        """Returns a new automaton whose language is the intersection of the
        language of this automaton and the language of the given
        automaton.

        Theorem 1.
        Suppose M_1 = (Q_1, \Sigma, q_1, A_1, \delta_1) and
        M_2 = (Q_2, \Sigma, q_2, A_2, \delta_2) are finite automata accepting
        L_1 and L_2 respectively. Let M be the FA (Q, \Sigma, q_0, A, \delta),
        where

                       Q = Q_1 x Q_2
                       q_0 = (q_1, q_2)

        and the transition function \delta is defined by the formula

                       \delta((p,q),\sigma) = (\delta_1(p,\sigma),\delta_2(q,\sigma))

        for every p \in Q_1, every q \in Q_2, and every \sigma  \in \Sigma. Then

                       If A = {(p,q) | p \in A_1 or q \in A_2},
                       M accepts the language L_1 \cap L_2.

        @param fa: A Finite Automata to intersect with.
        @type fa: FiniteAutomata.
        """

        def acceptCriteria(q, r):
            return q in self.accept and r in fa.accept

        return self._mergeAutomatas(fa, acceptCriteria)

    def union(self, fa):
        """Returns a new automaton whose language is the union of the
        language of this automaton and the language of the given
        automaton.

        (See description of intersection for further explanation).

                       If A = {(p,q) | p \in A_1 or q \in A_2},
                       M accepts the language L_1 \cup L_2.

        @param fa: A Finite Automata to union with.
        @type fa: FiniteAutomata.
        """

        def acceptCriteria(q, r):
            return q in self.accept or r in fa.accept

        return self._mergeAutomatas(fa, acceptCriteria)

    def minus(self, fa):
        """Returns a new automaton whose language is equal to the language of
        this automaton minus the language of the given automaton.

        (See description of intersection for further explanation).

                       If A = {(p,q) | p \in A_1 or q \in A_2},
                       M accepts the language L_1 - L_2.

        @param fa: A Finite Automata to union with.
        @type fa: FiniteAutomata.
        """

        def acceptCriteria(q, r):
            return q in self.accept and r not in fa.accept

        return self._mergeAutomatas(fa, acceptCriteria)

    def _mergeAutomatas(self, fa, acceptCriteria):
        """Merges this automata with the given automata based on the specified
        acceptCriteria.

        @param fa: A Finite Automata to union with.
        @type fa: FiniteAutomata.

        @param acceptCriteria: A function which takes two states as arguments
        and returns true if the composite state should be an accept state, false
        otherwise.
        @type acceptCriteria: function.
        """

        if self.alphabet != fa.alphabet:
            raise IllegalArgumentError(fa.alphabet)

        stateDictionary = {}
        stateList = []
        alphabet = self.alphabet
        initial = ''
        acceptList = []
        transitions = {}

        for q in self.states:
            for r in fa.states:
                state = q + r
                stateDictionary[(q,r)] = state

                if acceptCriteria(q,r):
                    acceptList.append(state)

        for statePair, compositeState in stateDictionary.items():
            stateList.append(compositeState)
            for character in alphabet:
                nextStateSelf = self.delta(statePair[0], character)
                nextStateFA = fa.delta(statePair[1], character)
                transitions[(compositeState,character)] = \
                    stateDictionary[(nextStateSelf, nextStateFA)]

        initial = stateDictionary[(self.initial, fa.initial)]
        states = frozenset(stateList)
        accept = frozenset(acceptList)

        return FiniteAutomata(states, alphabet, initial, accept, transitions)

    def toNondeterministicFiniteAutomata(self):
        """Converts this Finite Automata into an equivalent Nondeterministic
        Finite Automata."""
        return NondeterministicFiniteAutomata(self.states, self.alphabet,
        self.initial, self.accept, copy.copy(self.transitions))

    def toRegularExpression(self):
        """Converts this Automaton into an equivalent Regular Expression."""
        pass

    def _tableLookup(self, p, q, k, table, statemap):
        """Finds regular expression in table or computes it if not there yet."""
        pass


# end-of-finite_automata.py
