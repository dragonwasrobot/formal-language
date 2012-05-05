# exceptions.py

# Exceptions used in the automatas.
#
# Author: Peter Urbak
# Version: 2012-05-05

# --*-- Exceptions --*--

class IllegalArgumentError(Exception):
    """This error is raised when an illegal argument has been passed to a
    method."""

    def __init__(self, string):
        """Initializes an IllegalArgumentError object."""
        self.string = string

    def __str__(self):
        """Returns a the illegal argument."""
        return repr(self.string)

class IllegalCharacterError(Exception):
    """This error is raised whenever a character not found in a Finite Automatas
    alphabet is trying to be used in some method context."""

    def __init__(self, string):
        """Initializes an IllegalCharacterError object."""
        self.string = string

    def __str__(self):
        """Returns a description of the error which occured."""
        return repr(self.string)

class AutomatonNotWellDefinedError(Exception):
    """This error is raised whenever a automaton has not been correctly
    constructed according to its definition."""

    def __init__(self, string):
        """Initializes an IllegalCharacterError object."""
        self.string = string

    def __str__(self):
        """Returns the error message of the Exception."""
        return repr(self.string)

## end-of-exceptions.py
