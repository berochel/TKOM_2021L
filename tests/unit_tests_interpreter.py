import unittest

from my_parser.parser import Parser

import my_interpreter.lib_methods as lib
from lexer.source_read import TextSource
from my_interpreter.visitor import Visitor, Interpreter

TEST_SOURCE_1_LINE = '../test_files/test_interpreter_code.txt'


def put_line_in_lexer_text_source(parser, line):
    parser.lexer.textSource.text = line[1:]
    parser.lexer.current_char = line[0]
    parser.lexer.textSource._is_testing = True
    parser._next_token()


class InterpreterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser(64, 256, TextSource(TEST_SOURCE_1_LINE))

    def test_init_operation(self):
        textSource = TextSource(TEST_SOURCE_1_LINE)

        parser = Parser(64, 256, textSource)

        tree = parser.parse()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.interpret()

        printable = f'Returned {program.return_val}.'

        print(printable)

        self.assertEqual(printable, 'Returned 1296.')
