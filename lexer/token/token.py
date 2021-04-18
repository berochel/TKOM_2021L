#    Written by: Jarosław Zabuski, 2021

# Contains classes inplementing a single token object classes
# ,which differ, based on whether or not a lexical token has
# a value, which needs to be processed. Additionally, a Position
# class is implemented here, serving as a way to simplify future
# source text cursor position handling.

from lexer.token.types import TokenType


# Implements simple source text cursor position handling, like:
# location printing, printing the representation of itself,
# copying its data elsewhere, and overloading addition operators.
class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return f'({self.row}:{self.column})'

    def __add__(self, other):
        return Position(self.row, self.column + other)

    def __sub__(self, other):
        return Position(self.row, self.column - other)

    def print_location(self):
        return f'({self.row}:{self.column})'

    def copy(self):
        return Position(self.row, self.column)


# Class which serves as a base, single token representation.
# Handles token representation, checking for equality of its type
# with other tokens, and printing its position. Token creating by
# regex rules is handled in _find_matching_token in LexerMain class.
class Token:
    def __init__(self, type_: TokenType, start: Position = None, end: Position = None):
        self.type = type_
        self.start = start
        self.end = end

    def __repr__(self):
        return self.type.to_string()

    def __eq__(self, other):
        return True if self.type == other.type else False

    def print_location(self):
        if self.start is not None and self.end is not None:
            return f'starts at: {self.start.print_location()}  ,  ends at: {self.end.print_location()}'

        return 'at unspecified position'


# Class which serves as a representation of a more complex lexical tokens
# with values attached to them, according to their type. Handles literals
# and identifiers of classes, functions, variables etc.
# Overhauls BaseToken representations and equality methods.
class TokenWithValue(Token):
    def __init__(self, type_: TokenType, value, start: Position = None, end: Position = None):

        super().__init__(type_, start, end)
        self.value = value

    def __repr__(self):
        return f'{self.type.to_string()}: {self.value}'

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False


# Main token generation function. Checks whether or not the token type,
# found with regex rules, is meant to have a value, and creates according
# token.
def new_token(token_type: TokenType, value, start, end):

    if token_type.is_token_with_value():
        if token_type == TokenType.VT_INT:
            value = int(value)
        elif token_type == TokenType.VT_DOUBLE:
            value = float(value)
        elif token_type == TokenType.VT_STRING:
            value = str(value)
        return TokenWithValue(token_type, value, start, end)

    else:
        return Token(token_type, start, end)
