# exceptions.py

# Exceptions used in the automatas.
#
# Author: Peter Urbak
# Version: 2012-05-02

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

class AutomatonNotWellDefinedError(Exception):
    """This error is raised whenever a automaton has not been correctly
    constructed according to its definition."""

    def __init__(self, message):
        """Initializes an IllegalCharacterError object."""
        self.message = message

    def __str__(self):
        """Returns the error message of the Exception."""
        return repr(self.message)

## end-of-exceptions.py
