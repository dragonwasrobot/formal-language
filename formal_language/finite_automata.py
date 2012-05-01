# finite_automaata.py

# An implementation of a (Deterministic) Finite Automata.
# Finite Automatas are usually used in Formal Language Theory to reason about
# regular languages.
#
# Author: Peter Urbak
# Version: 2012-04-28
import copy

# --*-- The Finite Automata --*--

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

        # TODO: Sanitize input, especially alphabet symbols.

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
        automaton."""
        # TODO (chapter 2.6)
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
        # TODO (Dijkstra?)
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

        if self.alphabet != fa.alphabet:
            raise IllegalArgumentError(fa.alphabet)

        stateDictionary = {}
        stateList = []
        alphabet = self.alphabet
        initial = ''
        accept = []
        transitions = {}

        for q in self.states:
            for r in fa.states:
                state = q + r
                stateDictionary[(q,r)] = state

                if q in self.accept and r in fa.accept:
                    accept.append(state)

        for statePair, compositeState in stateDictionary.items():
            stateList.append(compositeState)
            for character in alphabet:
                nextStateSelf = self.delta(statePair[0], character)
                nextStateFA = fa.delta(statePair[1], character)
                transitions[(compositeState,character)] = \
                    stateDictionary[(nextStateSelf, nextStateFA)]

        initial = stateDictionary[(self.initial, fa.initial)]
        states = frozenset(stateList)

        return FiniteAutomata(states, alphabet, initial, accept, transitions)

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

        if self.alphabet != fa.alphabet:
            raise IllegalArgumentError(fa.alphabet)

        stateDictionary = {}
        stateList = []
        alphabet = self.alphabet
        initial = ''
        accept = []
        transitions = {}

        for q in self.states:
            for r in fa.states:
                state = q + r
                stateDictionary[(q,r)] = state

                if q in self.accept or r in fa.accept:
                    accept.append(state)

        for statePair, compositeState in stateDictionary.items():
            stateList.append(compositeState)
            for character in alphabet:
                nextStateSelf = self.delta(statePair[0], character)
                nextStateFA = fa.delta(statePair[1], character)
                transitions[(compositeState,character)] = \
                    stateDictionary[(nextStateSelf, nextStateFA)]

        initial = stateDictionary[(self.initial, fa.initial)]
        states = frozenset(stateList)

        return FiniteAutomata(states, alphabet, initial, accept, transitions)

    def minus(self, fa):
        """Returns a new automaton whose language is equal to the language of
        this automaton minus the language of the given automaton.

        (See description of intersection for further explanation).

                       If A = {(p,q) | p \in A_1 or q \in A_2},
                       M accepts the language L_1 - L_2.

        @param fa: A Finite Automata to union with.
        @type fa: FiniteAutomata.
        """

        if self.alphabet != fa.alphabet:
            raise IllegalArgumentError(fa.alphabet)

        stateDictionary = {}
        stateList = []
        alphabet = self.alphabet
        initial = ''
        accept = []
        transitions = {}

        for q in self.states:
            for r in fa.states:
                state = q + r
                stateDictionary[(q,r)] = state

                if q in self.accept and r not in fa.accept:
                    accept.append(state)

        for statePair, compositeState in stateDictionary.items():
            stateList.append(compositeState)
            for character in alphabet:
                nextStateSelf = self.delta(statePair[0], character)
                nextStateFA = fa.delta(statePair[1], character)
                transitions[(compositeState,character)] = \
                    stateDictionary[(nextStateSelf, nextStateFA)]

        initial = stateDictionary[(self.initial, fa.initial)]
        states = frozenset(stateList)

        return FiniteAutomata(states, alphabet, initial, accept, transitions)

# --*-- Exceptions --*--

class IllegalArgumentError(Exception):
    """This error is raised when an illegal argument has been passed to a
    method."""

    def __init__(self, argument):
        """Initializes an IllegalArgumentError object."""
        self.argument = argument

    def __str__(self):
        """Returns a the illegal argument."""
        return repr(self.argument)


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

'''
    /**
     * Returns <a href="http://www.research.att.com/sw/tools/graphviz/" target="_top">Graphviz Dot</a>
     * representation of this automaton.
     * (To convert a dot file to postscript, run '<tt>dot -Tps -o file.ps file.dot</tt>'.)
     */
    public String toDot()
    {
        StringBuffer b = new StringBuffer("digraph Automaton {\n");
        b.append("  rankdir = LR;\n");
        Map<State,Integer> id = new HashMap<State,Integer>();
        for (State s : states)
            id.put(s, Integer.valueOf(id.size()));
        for (State s : states) {
            b.append("  ").append(id.get(s));
            if (accept.contains(s))
                b.append(" [shape=doublecircle,label=\""+s.name+"\"];\n");
            else
                b.append(" [shape=circle,label=\""+s.name+"\"];\n");
            if (s==initial) {
                b.append("  in [shape=plaintext,label=\"\"];\n");
                b.append("  in -> ").append(id.get(s)).append(";\n");
            }
        }
        for (Map.Entry<StateSymbolPair,State> e : transitions.entrySet())
        {
            StateSymbolPair ssp = e.getKey();
            State q = e.getValue();
            b.append("  ").append(id.get(ssp.state)).append(" -> ").append(id.get(q));
            b.append(" [label=\"");
            char c = ssp.symbol.charValue();
            if (c>=0x21 && c<=0x7e && c!='\\' && c!='%')
                b.append(c);
            else
            {
                b.append("\\u");
                String s = Integer.toHexString(c);
                if (c<0x10)
                    b.append("000").append(s);
                else if (c<0x100)
                    b.append("00").append(s);
                else if (c<0x1000)
                    b.append("0").append(s);
                else
                    b.append(s);
            }
            b.append("\"];\n");
        }
        return b.append("}\n").toString();
    }


    public FA checkWellDefined() throws AutomatonNotWellDefinedException {
        if (states==null || alphabet==null || alphabet.symbols==null ||
            initial==null || accept==null || transitions==null)
            throw new AutomatonNotWellDefinedException("invalid null pointer");
        if (!states.contains(initial))
            throw new AutomatonNotWellDefinedException("the initial state is not in the state set");
        if (!states.containsAll(accept))
            throw new AutomatonNotWellDefinedException("not all accept states are in the state set");
        for (State s : states)
            for (char c : alphabet.symbols) {
                if (c==NFALambda.LAMBDA)
                    throw new AutomatonNotWellDefinedException("lambda transition appears in transitions");
                State s2 = transitions.get(new StateSymbolPair(s, c));
                if (s2==null)
                    throw new AutomatonNotWellDefinedException("transition function is not total");
                if (!states.contains(s2))
                    throw new AutomatonNotWellDefinedException("there is a transition to a state that is not in state set");
            }
        for (StateSymbolPair sp : transitions.keySet())
        {
            if (!states.contains(sp.state))
                throw new AutomatonNotWellDefinedException("transitions refer to a state not in the state set");
            if (!alphabet.symbols.contains(sp.symbol))
                throw new AutomatonNotWellDefinedException("non-alphabet symbol appears in transitions");
        }
        return this;
    }

}

/**
     * Finds regular expression in table or computes it if not there yet. (Used by {@link #toRegExp}.)
     */
    private RegExp.Node tableLookup(State p, State q, int k, Map<StatePair,RegExp.Node[]> table, Map<Integer,State> statemap) {
        RegExp.Node x = table.get(new StatePair(p, q))[k];
        if (x==null) {
            if (k==0) {
                x = new RegExp.EmptyLanguageNode();
                for (char c : alphabet.symbols)
                    if (delta(p,c)==q)
                        x = new RegExp.UnionNode(x, new RegExp.SymbolNode(c));
                if (p==q)
                    x = new RegExp.UnionNode(x, new RegExp.EmptyStringNode());
            } else {
                State r = statemap.get(k);
                RegExp.Node x1 = tableLookup(p, q, k-1, table, statemap);
                RegExp.Node x2 = tableLookup(p, r, k-1, table, statemap);
                RegExp.Node x3 = tableLookup(r, r, k-1, table, statemap);
                RegExp.Node x4 = tableLookup(r, q, k-1, table, statemap);
                x = new RegExp.UnionNode(x1, new RegExp.ConcatNode(x2, new RegExp.ConcatNode(new RegExp.StarNode(x3), x4)));

            }
            table.get(new StatePair(p, q))[k] = x;
        }
        return x;
    }

    /**
     * Converts this automaton into an equivalent {@link RegExp} regular expression. [Martin, Th. 3.30]
     */
    public RegExp toRegExp() {
        Map<Integer,State> statemap = new HashMap<Integer,State>();
        Map<StatePair,RegExp.Node[]> table = new HashMap<StatePair,RegExp.Node[]>(); // fill out this table lazily
        // initialize
        int n = 0;
        for (State p : states) {
            statemap.put(++n, p); // states are numbered from 1 to states.size()
            for (State q : states)
                table.put(new StatePair(p, q), new RegExp.Node[states.size()+1]);
        }
        // construct the abstract syntax tree for the regular expression
        RegExp.Node x = new RegExp.EmptyLanguageNode();
        for (State p : accept)
            x = new RegExp.UnionNode(x, tableLookup(initial, p, states.size(), table, statemap));
        return new RegExp(x, alphabet);
    }

'''
