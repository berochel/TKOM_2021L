#    Written by: Jarosław Zabuski, 2021

# Contains classes that list possible tokens and give, with the help of
# Dict[], a simple way to attribute them to regex rules listed at
# regex_rules.py.

import enum


class TokenType(enum.Enum):

    def is_token_with_value(self):
        return True if self.name.startswith("VALUE_") else False

    def is_token_a_keyword(self):
        return True if self.name.startswith("K_") else False

    def to_string(self):
        for key, value in token_type_repr.items():
            if self == value:
                return key

    # new line characters, tabulators, and whitespaces.
    IGNORE = enum.auto()

    # types
    K_INTEGER = enum.auto()
    K_DOUBLE = enum.auto()
    K_BOOLEAN = enum.auto()
    K_STRING = enum.auto()
    K_VOID = enum.auto()

    # punctuation symbols
    VERTICAL_LINE = enum.auto()
    AMPERSAND = enum.auto()
    EXCLAMATION = enum.auto()

    COMMA = enum.auto()
    LEFT_BRACKET = enum.auto()
    RIGHT_BRACKET = enum.auto()
    DOT = enum.auto()
    LEFT_PARENT = enum.auto()
    RIGHT_PARENT = enum.auto()
    SEMICOLON = enum.auto()
    COMMENT_SIGN = enum.auto()
    QUOTE = enum.auto()

    # math operators
    PLUS_OR_CONC = enum.auto()
    MINUS = enum.auto()
    MUL_OR_REFER = enum.auto()
    DIV = enum.auto()

    # logic operators
    LESS_EQUAL = enum.auto()
    LESS = enum.auto()
    GREATER_EQUAL = enum.auto()
    GREATER = enum.auto()
    EQUAL = enum.auto()
    NOT_EQUAL = enum.auto()

    # other terminal symbols
    K_IF = enum.auto()
    K_ELSE = enum.auto()
    K_CLASS = enum.auto()
    K_RETURN = enum.auto()
    K_WHILE = enum.auto()
    ASSIGN_OP = enum.auto()
    K_TRUE = enum.auto()
    K_FALSE = enum.auto()
    EOT = enum.auto()
    UNKNOWN = enum.auto()

    # constant values
    VALUE_DOUBLE = enum.auto()
    VALUE_INT = enum.auto()
    VALUE_STRING = enum.auto()
    VALUE_COMMENT = enum.auto()
    VALUE_NUMBER = enum.auto()

    # identifiers
    VALUE_ID = enum.auto()


token_type_repr = {

    'Integer': TokenType.K_INTEGER,
    'Double': TokenType.K_DOUBLE,
    'Boolean': TokenType.K_BOOLEAN,
    'String': TokenType.K_STRING,
    'Void': TokenType.K_VOID,

    '|': TokenType.VERTICAL_LINE,
    '&': TokenType.AMPERSAND,
    '!': TokenType.EXCLAMATION,

    ',': TokenType.COMMA,
    '{': TokenType.LEFT_BRACKET,
    '}': TokenType.RIGHT_BRACKET,
    '.': TokenType.DOT,
    '(': TokenType.LEFT_PARENT,
    ')': TokenType.RIGHT_PARENT,
    ';': TokenType.SEMICOLON,
    '"': TokenType.QUOTE,

    '+': TokenType.PLUS_OR_CONC,
    '-': TokenType.MINUS,
    '*': TokenType.MUL_OR_REFER,
    '/': TokenType.DIV,

    '<': TokenType.LESS,
    '>': TokenType.GREATER,
    '<=': TokenType.LESS_EQUAL,
    '>=': TokenType.GREATER_EQUAL,
    '!=': TokenType.NOT_EQUAL,
    '==': TokenType.EQUAL,

    'if': TokenType.K_IF,
    'else': TokenType.K_ELSE,
    'class': TokenType.K_CLASS,
    'return': TokenType.K_RETURN,
    'while': TokenType.K_WHILE,
    '=': TokenType.ASSIGN_OP,
    'true': TokenType.K_TRUE,
    'false': TokenType.K_FALSE,
    'End of text': TokenType.EOT,
    'Unknown': TokenType.UNKNOWN,

    'Double literal': TokenType.VALUE_DOUBLE,
    'Int literal': TokenType.VALUE_INT,
    'String literal': TokenType.VALUE_STRING,
    'Comment': TokenType.VALUE_COMMENT,
    'Number literal': TokenType.VALUE_NUMBER,

    'Identifier': TokenType.VALUE_ID,

}
parameter_types = [TokenType.K_INTEGER,
                   TokenType.K_STRING,
                   TokenType.K_DOUBLE,
                   TokenType.K_BOOLEAN]

function_types = [TokenType.K_INTEGER,
                  TokenType.K_STRING,
                  TokenType.K_DOUBLE,
                  TokenType.K_BOOLEAN,
                  TokenType.K_VOID]
