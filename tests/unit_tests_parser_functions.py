import unittest

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


if __name__ == '__main__':
    unittest.main()
