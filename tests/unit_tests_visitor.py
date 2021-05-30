import unittest

from my_parser.parser import Parser

import my_interpreter.lib_methods as lib
from lexer.source_read import TextSource
from my_interpreter.scope_manager import Scope
from my_interpreter.visitor import Visitor, Interpreter

TEST_SOURCE_1_LINE = '../test_files/test_lexer_singleLineReadExample.txt'


def put_line_in_lexer_text_source(parser, line):
    parser.lexer.textSource.text = line[1:]
    parser.lexer.current_char = line[0]
    parser.lexer.textSource._is_testing = True
    parser._next_token()


class VisitorOperationsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser(64, 256, TextSource(TEST_SOURCE_1_LINE))

    def test_init_operation(self):
        line = "Integer i = 2; "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_init()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_init_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, 2)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {'i': 2})

    def test_return_operation(self):
        line = "return 2; "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_return()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_return_stat_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, 2)
        self.assertEqual(program.visitor.scope_manager.return_result, 2)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_condition_operation(self):
        line = "2 < 3 "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_condition()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_less_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, True)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

        program.visitor._visit_greater_equal_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, False)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

        program.visitor._visit_less_equal_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, True)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

        program.visitor._visit_greater_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, False)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_mul_operation(self):
        line = "6 * 8 "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_expression()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_mul_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, 48)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_div_operation(self):
        line = "6 / 8 "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_expression()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_div_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, 0.75)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_add_operation(self):
        line = "6 + 8 "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_expression()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_add_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, 14)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_sub_operation(self):
        line = "6 - 8 "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_expression()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_sub_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, -2)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_if_else_operation(self):
        line = "if (2 > 3) { Integer a = 2; } else { Double temp = 3.0; return temp; } "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_if()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_if_else_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, 3.0)
        self.assertEqual(program.visitor.scope_manager.return_result, 3.0)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})

    def test_if_else_operation2(self):
        line = "if (2 < 3) { Integer a = 2; } else { Double temp = 3.0; return temp; } "
        put_line_in_lexer_text_source(self.parser, line)

        tree = self.parser._parse_if()

        visitor = Visitor(tree)

        program = Interpreter(visitor, lib)

        program.visitor.scope_manager.scope_stack[1].append(Scope('test'))

        program.visitor._visit_if_else_operation(tree)

        self.assertEqual(program.visitor.scope_manager.last_operation_result, None)
        self.assertEqual(program.visitor.scope_manager.return_result, None)
        self.assertEqual(program.visitor.scope_manager.scope_stack[1][0].vars_or_attrs, {})
