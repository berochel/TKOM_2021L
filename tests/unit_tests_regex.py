#    Written by: Jarosław Zabuski, 2021

# Contains tests checking the actions performed by regex rules and token handling classes.
# Checks whether or not every single token behaves as intended.

import re
import unittest

from lexer.token.regex_rules import regexRules
from lexer.token.token import Token, TokenWithValue
from lexer.token.types import TokenType


class TestRegex(unittest.TestCase):
    def setUp(self) -> None:

        self.regexRules = regexRules
        self.regexRules_compiled = {}

        for regex in regexRules:
            regex_compiled = re.compile(regex)
            self.regexRules_compiled[regex_compiled] = regexRules[regex]

    def find_token(self, line):

        token_args = self._find_token_args(line)
        if not token_args:
            return None

        token_type, value = token_args
        if token_type.is_token_with_value():
            token = TokenWithValue(token_type, value)
        else:
            token = Token(token_type)

        return token

    def _find_token_args(self, line):

        for regex in self.regexRules_compiled:
            match = regex.match(line)

            if match:
                token_type = self.regexRules_compiled[regex]
                value = match.group(0)
                return token_type, value

        return None

    def test_double_value(self):

        line = "2.5"

        found_token = self.find_token(line)
        expected = TokenWithValue(TokenType.VT_DOUBLE, "2.5")
        self.assertEqual(expected, found_token)

    def test_string_value(self):

        line = '"test string"'

        found_token = self.find_token(line)
        expected = TokenWithValue(TokenType.VT_STRING, '"test string"')
        self.assertEqual(expected, found_token)

    def test_int_value(self):

        line = "152"

        found_token = self.find_token(line)
        expected = TokenWithValue(TokenType.VT_INT, "152")
        self.assertEqual(expected, found_token)

    def test_int(self):

        line = "Integer"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_INTEGER)
        self.assertEqual(expected, found_token)

    def test_double(self):

        line = "Double"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_DOUBLE)
        self.assertEqual(expected, found_token)

    def test_string(self):

        line = "String"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_STRING)
        self.assertEqual(expected, found_token)

    def test_bool(self):

        line = "Boolean"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_BOOLEAN)
        self.assertEqual(expected, found_token)

    def test_comma(self):

        line = ","

        found_token = self.find_token(line)
        expected = Token(TokenType.T_COMMA)
        self.assertEqual(expected, found_token)

    def test_dot(self):

        line = "."

        found_token = self.find_token(line)
        expected = Token(TokenType.T_DOT)
        self.assertEqual(expected, found_token)

    def test_semicolon(self):

        line = ";"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_SEMICOLON)
        self.assertEqual(expected, found_token)

    def test_lbracket(self):

        line = "{"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_LEFT_BRACKET)
        self.assertEqual(expected, found_token)

    def test_rbracket(self):

        line = "}"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_RIGHT_BRACKET)
        self.assertEqual(expected, found_token)

    def test_lparent(self):

        line = "("

        found_token = self.find_token(line)
        expected = Token(TokenType.T_LEFT_PARENT)
        self.assertEqual(expected, found_token)

    def test_rparent(self):

        line = ")"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_RIGHT_PARENT)
        self.assertEqual(expected, found_token)

    def test_plus(self):

        line = "+"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_PLUS_OR_CONC)
        self.assertEqual(expected, found_token)

    def test_minus(self):

        line = "-"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_MINUS)
        self.assertEqual(expected, found_token)

    def test_mul(self):

        line = "*"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_MUL_OR_REFER)
        self.assertEqual(expected, found_token)

    def test_div(self):

        line = "/"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_DIV)
        self.assertEqual(expected, found_token)

    def test_less_or_eq(self):

        line = "<="

        found_token = self.find_token(line)
        expected = Token(TokenType.T_LESS_EQUAL)
        self.assertEqual(expected, found_token)

    def test_less(self):

        line = "<"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_LESS)
        self.assertEqual(expected, found_token)

    def test_eq(self):

        line = "=="

        found_token = self.find_token(line)
        expected = Token(TokenType.T_EQUAL)
        self.assertEqual(expected, found_token)

    def test_not_eq(self):

        line = "!="

        found_token = self.find_token(line)
        expected = Token(TokenType.T_NOT_EQUAL)
        self.assertEqual(expected, found_token)

    def test_greater_or_eq(self):

        line = ">="

        found_token = self.find_token(line)
        expected = Token(TokenType.T_GREATER_EQUAL)
        self.assertEqual(expected, found_token)

    def test_greater(self):

        line = ">"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_GREATER)
        self.assertEqual(expected, found_token)

    def test_if(self):

        line = "if"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_IF)
        self.assertEqual(expected, found_token)

    def test_else(self):

        line = "else"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_ELSE)
        self.assertEqual(expected, found_token)

    def test_true(self):

        line = "true"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_TRUE)
        self.assertEqual(expected, found_token)

    def test_false(self):

        line = "false"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_FALSE)
        self.assertEqual(expected, found_token)

    def test_return(self):

        line = "return"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_RETURN)
        self.assertEqual(expected, found_token)

    def test_while(self):

        line = "while"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_WHILE)
        self.assertEqual(expected, found_token)

    def test_assign(self):

        line = "="

        found_token = self.find_token(line)
        expected = Token(TokenType.T_ASSIGN_OP)
        self.assertEqual(expected, found_token)

    def test_void(self):

        line = "Void"

        found_token = self.find_token(line)
        expected = Token(TokenType.T_VOID)
        self.assertEqual(expected, found_token)


if __name__ == '__main__':
    unittest.main()
