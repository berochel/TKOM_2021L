#    Written by: Jarosław Zabuski, 2021

# Contains all regex rules, needed to parse source text into tangible tokens.

import re

from lexer.token.types import TokenType


def compile_regex():

    regexRules_compiled = {}

    for regex in regexRules:
        compiled_regex = re.compile(regex)
        regexRules_compiled[compiled_regex] = regexRules[regex]

    return regexRules_compiled


regexRules = {

    r'\n': TokenType.T_IGNORE,  # new line character
    r'[ \t]+': TokenType.T_IGNORE,  # one or more space or tab characters

    r'Double(?![\w\d])': TokenType.T_DOUBLE,  # valid "Double" keyword.
    r'Integer(?![\w\d])': TokenType.T_INTEGER,  # valid "Integer" keyword.
    r'Boolean(?![\w\d])': TokenType.T_BOOLEAN,  # valid "Boolean" keyword.
    r'String(?![\w\d])': TokenType.T_STRING,  # valid "String" keyword.
    r'Void(?![\w\d])': TokenType.T_VOID,  # valid "Void" keyword.

    r',': TokenType.T_COMMA,
    r'\{': TokenType.T_LEFT_BRACKET,
    r'\}': TokenType.T_RIGHT_BRACKET,
    r'\.': TokenType.T_DOT,
    r'\(': TokenType.T_LEFT_PARENT,
    r'\)': TokenType.T_RIGHT_PARENT,
    r';': TokenType.T_SEMICOLON,
    r'\/\/': TokenType.T_COMMENT_SIGN,

    r'\+': TokenType.T_PLUS_OR_CONC,
    r'-': TokenType.T_MINUS,
    r'\*': TokenType.T_MUL_OR_REFER,
    r'/': TokenType.T_DIV,

    r'<=': TokenType.T_LESS_EQUAL,
    r'<': TokenType.T_LESS,
    r'>=': TokenType.T_GREATER_EQUAL,
    r'>': TokenType.T_GREATER,
    r'==': TokenType.T_EQUAL,
    r'!=': TokenType.T_NOT_EQUAL,

    r'\|': TokenType.T_VERTICAL_LINE,
    r'&': TokenType.T_AMPERSAND,
    r'!': TokenType.T_EXCLAMATION,

    r'if(?![\w\d])': TokenType.T_IF,  # valid "if" keyword.
    r'else(?![\w\d])': TokenType.T_ELSE,  # valid "else" keyword.
    r'class(?![\w\d])': TokenType.T_CLASS,  # valid "class" keyword.
    r'return(?![\w\d])': TokenType.T_RETURN,  # valid "return" keyword.
    r'while(?![\w\d])': TokenType.T_WHILE,  # valid "while" keyword.
    r'=': TokenType.T_ASSIGN_OP,
    r'true(?![\w\d])': TokenType.T_TRUE,  # valid "true" keyword.
    r'false(?![\w\d])': TokenType.T_FALSE,  # valid "false" keyword.
    r'DONE(?![\w\d])': TokenType.T_EOT,  # valid "DONE" keyword, used for stdin input source code.

    r'[a-zA-Z_][a-zA-Z0-9_]*': TokenType.VT_ID,  # valid identifier.

    r'\d+\.\d+(?![\w])': TokenType.VT_DOUBLE,  # valid Double value.
    r'(0|[1-9]\d*)(?![\w])': TokenType.VT_INT,  # valid Int value.
    r'(")([^"\\]*(?:\\.[^"\\]*)*)(")(?![\w])': TokenType.VT_STRING  # valid String value, which escapes the " symbol.

}
