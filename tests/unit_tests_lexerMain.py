#    Written by: Jarosław Zabuski, 2021

# Contains tests checking the actions performed by regex rules and token handling classes.
# Checks if the lexer appropriately build lexical trees based on lines of source text.

import unittest

from lexer.lexer import LexerMain
from lexer.token.token import Token, TokenWithValue
from lexer.token.types import TokenType


class LexerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.lexer = LexerMain()

    def test_types(self):

        line = "Integer Double Boolean String Void"

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_INTEGER),
                    Token(TokenType.T_DOUBLE),
                    Token(TokenType.T_BOOLEAN),
                    Token(TokenType.T_STRING),
                    Token(TokenType.T_VOID)
                    ]
        self.assertEqual(expected, operation)

    def test_punctuation(self):

        line = ", . ; { } ( )"

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_COMMA),
                    Token(TokenType.T_DOT),
                    Token(TokenType.T_SEMICOLON),
                    Token(TokenType.T_LEFT_BRACKET),
                    Token(TokenType.T_RIGHT_BRACKET),
                    Token(TokenType.T_LEFT_PARENT),
                    Token(TokenType.T_RIGHT_PARENT)]
        self.assertEqual(expected, operation)

    def test_math_operators(self):

        line = "+ - * /"

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_PLUS_OR_CONC),
                    Token(TokenType.T_MINUS),
                    Token(TokenType.T_MUL_OR_REFER),
                    Token(TokenType.T_DIV)]
        self.assertEqual(expected, operation)

    def test_equality_operators(self):

        line = "<= < >= > == !="

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_LESS_EQUAL),
                    Token(TokenType.T_LESS),
                    Token(TokenType.T_GREATER_EQUAL),
                    Token(TokenType.T_GREATER),
                    Token(TokenType.T_EQUAL),
                    Token(TokenType.T_NOT_EQUAL)]
        self.assertEqual(expected, operation)

    def test_logic_operators(self):

        line = "| &"

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_VERTICAL_LINE),
                    Token(TokenType.T_AMPERSAND)]
        self.assertEqual(expected, operation)

    def test_other_tokens(self):

        line = "if else true false return while ="

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_IF),
                    Token(TokenType.T_ELSE),
                    Token(TokenType.T_TRUE),
                    Token(TokenType.T_FALSE),
                    Token(TokenType.T_RETURN),
                    Token(TokenType.T_WHILE),
                    Token(TokenType.T_ASSIGN_OP)]
        self.assertEqual(expected, operation)

    def test_values(self):

        line = "\"string\" 5 2.5"

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [Token(TokenType.T_QUOTE),
                    TokenWithValue(TokenType.VT_STRING, 'string'),
                    Token(TokenType.T_QUOTE),
                    TokenWithValue(TokenType.VT_INT, 5),
                    TokenWithValue(TokenType.VT_DOUBLE, 2.5)]
        self.assertEqual(expected, operation)

    def test_ident(self):

        line = "var_name x y z"

        operation = self.lexer.get_tokens_from_specified_line(line)
        expected = [TokenWithValue(TokenType.VT_ID, "var_name"),
                    TokenWithValue(TokenType.VT_ID, "x"),
                    TokenWithValue(TokenType.VT_ID, "y"),
                    TokenWithValue(TokenType.VT_ID, "z")]
        self.assertEqual(expected, operation)


if __name__ == '__main__':
    unittest.main()
