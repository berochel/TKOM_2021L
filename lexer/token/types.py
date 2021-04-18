#    Written by: Jarosław Zabuski, 2021

# Contains classes that list possible tokens and give, with the help of
# Dict[], a simple way to attribute them to regex rules listed at
# regex_rules.py.

import enum

class TokenType(enum.Enum):

    def is_token_with_value(self):
        return True if self.name.startswith("V") else False

    def to_string(self):
        return token_type_repr.get(self)

    # new line characters, tabulators, and whitespaces.
    T_IGNORE = enum.auto()

    # types
    T_INTEGER = enum.auto()
    T_DOUBLE = enum.auto()
    T_BOOLEAN = enum.auto()
    T_STRING = enum.auto()
    T_VOID = enum.auto()

    # punctuation symbols
    T_VERTICAL_LINE = enum.auto()
    T_AMPERSAND = enum.auto()
    T_EXCLAMATION = enum.auto()

    T_COMMA = enum.auto()
    T_LEFT_BRACKET = enum.auto()
    T_RIGHT_BRACKET = enum.auto()
    T_DOT = enum.auto()
    T_LEFT_PARENT = enum.auto()
    T_RIGHT_PARENT = enum.auto()
    T_SEMICOLON = enum.auto()
    T_COMMENT_SIGN = enum.auto()
    T_QUOTE = enum.auto()

    # math operators
    T_PLUS_OR_CONC = enum.auto()
    T_MINUS = enum.auto()
    T_MUL_OR_REFER = enum.auto()
    T_DIV = enum.auto()

    # logic operators
    T_LESS_EQUAL = enum.auto()
    T_LESS = enum.auto()
    T_GREATER_EQUAL = enum.auto()
    T_GREATER = enum.auto()
    T_EQUAL = enum.auto()
    T_NOT_EQUAL = enum.auto()

    # other terminal symbols
    T_IF = enum.auto()
    T_ELSE = enum.auto()
    T_CLASS = enum.auto()
    T_RETURN = enum.auto()
    T_WHILE = enum.auto()
    T_ASSIGN_OP = enum.auto()
    T_TRUE = enum.auto()
    T_FALSE = enum.auto()
    T_EOT = enum.auto()

    # constant values
    VT_DOUBLE = enum.auto()
    VT_INT = enum.auto()
    VT_STRING = enum.auto()
    VT_COMMENT = enum.auto()

    # identifiers
    VT_ID = enum.auto()


token_type_repr = {

    TokenType.T_INTEGER: 'Integer',
    TokenType.T_DOUBLE: 'Double',
    TokenType.T_BOOLEAN: 'Boolean',
    TokenType.T_STRING: 'String',
    TokenType.T_VOID: 'Void',

    TokenType.T_VERTICAL_LINE: '|',
    TokenType.T_AMPERSAND: '&',
    TokenType.T_EXCLAMATION: '!',

    TokenType.T_COMMA: ',',
    TokenType.T_LEFT_BRACKET: '{',
    TokenType.T_RIGHT_BRACKET: '}',
    TokenType.T_DOT: '.',
    TokenType.T_LEFT_PARENT: '(',
    TokenType.T_RIGHT_PARENT: ')',
    TokenType.T_SEMICOLON: ';',
    TokenType.T_QUOTE: '"',
    TokenType.T_COMMENT_SIGN: '//',

    TokenType.T_PLUS_OR_CONC: '+',
    TokenType.T_MINUS: '-',
    TokenType.T_MUL_OR_REFER: '*',
    TokenType.T_DIV: '/',

    TokenType.T_LESS_EQUAL: '<=',
    TokenType.T_LESS: '<',
    TokenType.T_GREATER_EQUAL: '>=',
    TokenType.T_GREATER: '>',
    TokenType.T_EQUAL: '==',
    TokenType.T_NOT_EQUAL: '!=',

    TokenType.T_IF: 'if',
    TokenType.T_ELSE: 'else',
    TokenType.T_CLASS: 'class',
    TokenType.T_RETURN: 'return',
    TokenType.T_WHILE: 'while',
    TokenType.T_ASSIGN_OP: '=',
    TokenType.T_TRUE: 'true',
    TokenType.T_FALSE: 'false',
    TokenType.T_EOT: 'End of text',

    TokenType.VT_DOUBLE: 'Double literal',
    TokenType.VT_INT: 'Int literal',
    TokenType.VT_STRING: 'String literal',
    TokenType.VT_COMMENT: 'Comment',

    TokenType.VT_ID: 'Identifier',

}
