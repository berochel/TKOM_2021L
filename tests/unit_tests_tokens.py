#    Written by: Jarosław Zabuski, 2021

# Contains tests checking the actions performed by regex rules and tokens handling classes.
# Checks if the lexern appropriately build lexical trees based on lines of source text.

import unittest

from lexer.lexer import LexerMain
from lexer.source_read import TextSource
from lexer.token import Token, TokenWithValue, TokenWithDoubleValue
from lexer.types import TokenType

TEST_SOURCE_1_LINE = '../test_files/test_lexer_singleLineReadExample.txt'


def put_line_in_lexer_text_source(lexer, line):
    lexer.textSource.text = line[1:]
    lexer.current_char = line[0]
    lexer.textSource._is_testing = True


class LexerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.lexer = LexerMain(maxIdentLength=64, maxStringLength=256,
                               textSource=TextSource(TEST_SOURCE_1_LINE))

    def test_types(self):

        tokens = []
        line = "Integer Double Boolean String Void"
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        token = self.lexer.get_token()
        tokens.append(token)

        token = self.lexer.get_token()
        tokens.append(token)

        expected = [Token(TokenType.K_INTEGER),
                    Token(TokenType.K_DOUBLE),
                    Token(TokenType.K_BOOLEAN),
                    Token(TokenType.K_STRING),
                    Token(TokenType.K_VOID),
                    Token(TokenType.EOT),
                    Token(TokenType.EOT),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_punctuation(self):

        tokens = []
        line = ", . ; { } ( )  "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [Token(TokenType.COMMA),
                    Token(TokenType.DOT),
                    Token(TokenType.SEMICOLON),
                    Token(TokenType.LEFT_BRACKET),
                    Token(TokenType.RIGHT_BRACKET),
                    Token(TokenType.LEFT_PARENT),
                    Token(TokenType.RIGHT_PARENT),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_math_operators(self):

        tokens = []
        line = "+ - * / "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [Token(TokenType.PLUS_OR_CONC),
                    Token(TokenType.MINUS),
                    Token(TokenType.MUL_OR_REFER),
                    Token(TokenType.DIV),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_equality_operators(self):

        tokens = []
        line = "<= < >= > == !="
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [Token(TokenType.LESS_EQUAL),
                    Token(TokenType.LESS),
                    Token(TokenType.GREATER_EQUAL),
                    Token(TokenType.GREATER),
                    Token(TokenType.EQUAL),
                    Token(TokenType.NOT_EQUAL),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_comment_eot_handling(self):

        tokens = []
        line = "//to jest komentarz "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_logic_operators(self):

        tokens = []
        line = "| & ! "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [Token(TokenType.VERTICAL_LINE),
                    Token(TokenType.AMPERSAND),
                    Token(TokenType.EXCLAMATION),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_other_tokens(self):

        tokens = []
        line = "if else true false return while = "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [Token(TokenType.K_IF),
                    Token(TokenType.K_ELSE),
                    Token(TokenType.K_TRUE),
                    Token(TokenType.K_FALSE),
                    Token(TokenType.K_RETURN),
                    Token(TokenType.K_WHILE),
                    Token(TokenType.ASSIGN_OP),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_values(self):

        tokens = []
        line = "\"string\" 5 2.5 "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [TokenWithValue(TokenType.VALUE_STRING, 'string'),
                    TokenWithValue(TokenType.VALUE_INT, 5),
                    TokenWithDoubleValue(TokenType.VALUE_DOUBLE, 2, None, 5, 1),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_zero_values(self):

        tokens = []
        line = "0 0.0 0.000001"
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [TokenWithValue(TokenType.VALUE_INT, 0),
                    TokenWithDoubleValue(TokenType.VALUE_DOUBLE, 0, None, 0, 1),
                    TokenWithDoubleValue(TokenType.VALUE_DOUBLE, 0, None, 1, 6),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)

    def test_zero_error_raises(self):

        tokens = []
        line = "00000.0"
        put_line_in_lexer_text_source(self.lexer, line)

        try:
            while not self.lexer.is_eot_token():
                token = self.lexer.get_token()
                tokens.append(token)
        except Exception as exp:
            # testing both if error is raised correctly at unvalid zero value,
            # and if it raises at a correct position
            self.assertEqual(exp.message, "Unable to recognize: \"0\" at: (1:1)")

    def test_string_raises(self):

        # Checks if the exceeding max string length is raised correctly
        # for the default value of maxStringLength, that is, 256.
        tokens = []
        line = "\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\""
        put_line_in_lexer_text_source(self.lexer, line)

        try:
            while not self.lexer.is_eot_token():
                token = self.lexer.get_token()
                tokens.append(token)
        except Exception as exp:
            # testing both if error is raised correctly at unvalid zero value,
            # and if it raises at a correct position (column position has to be
            # equal to maxStringSize + 1)
            self.assertEqual(exp.message,
                             "Unable to recognize: \"A\" at: (1:257) (Exceeded maximum length of a string literal)")

    def test_identifier_raises(self):

        # Checks if the exceeding max string length is raised correctly
        # for the default value of maxIdentLength, that is, 64.
        tokens = []
        line = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        put_line_in_lexer_text_source(self.lexer, line)

        try:
            while not self.lexer.is_eot_token():
                token = self.lexer.get_token()
                tokens.append(token)
        except Exception as exp:
            # testing both if error is raised correctly at unvalid zero value,
            # and if it raises at a correct position (column position has to be
            # equal to maxIdentSize)
            self.assertEqual(exp.message,
                             "Unable to recognize: \"A\" at: (1:64) (Exceeded maximum length of a identifier literal)")

    def test_ident(self):

        tokens = []
        line = "var_name x y z "
        put_line_in_lexer_text_source(self.lexer, line)

        while not self.lexer.is_eot_token():
            token = self.lexer.get_token()
            tokens.append(token)

        expected = [TokenWithValue(TokenType.VALUE_ID, "var_name"),
                    TokenWithValue(TokenType.VALUE_ID, "x"),
                    TokenWithValue(TokenType.VALUE_ID, "y"),
                    TokenWithValue(TokenType.VALUE_ID, "z"),
                    Token(TokenType.EOT)
                    ]
        self.assertEqual(expected, tokens)


if __name__ == '__main__':
    unittest.main()
