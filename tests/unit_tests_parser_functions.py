import unittest

import nodes
from my_parser.parser import Parser

from lexer.source_read import TextSource
from lexer.types import TokenType

TEST_SOURCE_1_LINE = '../test_files/test_lexer_singleLineReadExample.txt'


def put_line_in_lexer_text_source(parser, line):
    parser.lexer.textSource.text = line[1:]
    parser.lexer.current_char = line[0]
    parser.lexer.textSource._is_testing = True
    parser._next_token()


class ParserFunctionsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser(64, 256, TextSource(TEST_SOURCE_1_LINE))

    def test_types(self):
        line = "Integer String Void"
        put_line_in_lexer_text_source(self.parser, line)

        par_type = self.parser._parse_parameter_type()

        expected = TokenType.K_INTEGER

        self.assertEqual(expected, par_type)

        par_type = self.parser._parse_function_type()

        expected = TokenType.K_STRING

        self.assertEqual(expected, par_type)

        par_type = self.parser._parse_parameter_type()

        expected = None

        self.assertEqual(expected, par_type)

    def test_variable_or_method_detection(self):
        line = "a a.b a() a.b() "
        put_line_in_lexer_text_source(self.parser, line)

        par_type = self.parser._parse_variable_or_method()

        expected = nodes.Variable("a")

        self.assertEqual(expected, par_type)

        par_type = self.parser._parse_variable_or_method()

        expected = nodes.ObjectVariable("a", ["b"])

        self.assertEqual(expected, par_type)

        par_type = self.parser._parse_variable_or_method()

        expected = nodes.FunctionCall(nodes.Variable("a"), [None])

        self.assertEqual(expected, par_type)

        par_type = self.parser._parse_variable_or_method()

        expected = nodes.ObjectMethod("a", ["b"], [None])

        self.assertEqual(expected, par_type)

    def test_next_token(self):
        line = "a b "
        put_line_in_lexer_text_source(self.parser, line)

        par = self.parser._next_token(TokenType.VALUE_ID)

        self.assertEqual(par, True)

        try:
            par = self.parser._next_token(TokenType.VALUE_INT)

        except Exception as exp:
            self.assertEqual(exp.message,
                             "Unexpected: \"Identifier: b\" at: (1:6)Expected:TokenType.VALUE_INT, got:Identifier: b")

    def test_expression(self):
        line = "a * 2 + 6 / b() "
        put_line_in_lexer_text_source(self.parser, line)

        par = self.parser._parse_expression()

        self.assertEqual(par.left.left.name, "a")
        self.assertEqual(par.left.right.value, 2)
        self.assertEqual(par.right.left.value, 6)
        self.assertEqual(par.right.right, nodes.FunctionCall(nodes.Variable("b"), [None]))

    def test_condition(self):
        line = "true | b & a != ! c <= 3 "
        put_line_in_lexer_text_source(self.parser, line)

        par = self.parser._parse_condition()

        self.assertEqual(par.__class__.__name__, "OrOperation")
        self.assertEqual(par.left.value, "true")
        self.assertEqual(par.right.__class__.__name__, "AndOperation")
        self.assertEqual(par.right.left, nodes.Variable("b"))
        self.assertEqual(par.right.right.__class__.__name__, "NotEqualOperation")
        self.assertEqual(par.right.right.left, nodes.Variable("a"))
        self.assertEqual(par.right.right.right.__class__.__name__, "NotOperation")
        self.assertEqual(par.right.right.right.right.__class__.__name__, "LessEqualOperation")
        self.assertEqual(par.right.right.right.right.left, nodes.Variable("c"))
        self.assertEqual(par.right.right.right.right.right.value, 3)

if __name__ == '__main__':
    unittest.main()
