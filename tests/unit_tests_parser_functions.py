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
        expected = nodes.FunctionCall(nodes.Variable("a"), [])
        self.assertEqual(expected, par_type)

        par_type = self.parser._parse_variable_or_method()
        expected = nodes.ObjectMethod("a", ["b"], [])
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
        self.assertEqual(par.right.right, nodes.FunctionCall(nodes.Variable("b"), []))

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

    def test_block_parsing(self):
        line = "{ Integer b = 10; return 0; if (a <= 10) {a = a + b;}} "
        put_line_in_lexer_text_source(self.parser, line)

        par = self.parser._parse_block()

        self.assertEqual(par[0].__class__.__name__, "InitStat")
        self.assertEqual(par[0].name, "b")
        self.assertEqual(par[0].type, TokenType.K_INTEGER)
        self.assertEqual(par[0].right.__class__.__name__, "Integer")
        self.assertEqual(par[0].right.value, 10)

        self.assertEqual(par[1].__class__.__name__, "ReturnStat")
        self.assertEqual(par[1].return_value.__class__.__name__, "Integer")
        self.assertEqual(par[1].return_value.value, 0)

        self.assertEqual(par[2].__class__.__name__, "IfElseStat")
        self.assertEqual(par[2].condition.__class__.__name__, "LessEqualOperation")
        self.assertEqual(par[2].condition.left, nodes.Variable("a"))
        self.assertEqual(par[2].condition.right.value, 10)

        self.assertEqual(par[2].instructions[0].__class__.__name__, "AssignStat")
        self.assertEqual(par[2].instructions[0].left, nodes.Variable("a"))
        self.assertEqual(par[2].instructions[0].right.__class__.__name__, "AddOperation")
        self.assertEqual(par[2].instructions[0].right.left, nodes.Variable("a"))
        self.assertEqual(par[2].instructions[0].right.right, nodes.Variable("b"))

    def test(self):
        line = "class Klasa{Integer a = 0;Integer b;Boolean c;Integer someMethod(){a = a + b;return a;}Void addOne(" \
               "Integer * x){x = x + 1;}} "
        put_line_in_lexer_text_source(self.parser, line)

        par = self.parser._parse_class_definition().__repr__()

        expected = "{\'Klasa\': Class:\nName:Klasa\nVariables:\nInit " \
                   "statement:\nType:\nTokenType.K_INTEGER\nName:\na\nAssigned:\nInteger:\n0\nInit " \
                   "statement:\nType:\nTokenType.K_INTEGER\nName:\nb\nInit " \
                   "statement:\nType:\nTokenType.K_BOOLEAN\nName:\nc\nMethods:\nFunction:\nName:someMethod\nType" \
                   ":TokenType.K_INTEGER\nParameters:\nInstructions:\nAssign:\nLeft assign " \
                   "operand:\nVariable:\na\nRight assign operand:\nAdd:\nLeft add operand:\nVariable:\na\nRight add " \
                   "operand:\nVariable:\nb\nReturn statement:\nReturn " \
                   "value:\nVariable:\na\nFunction:\nName:addOne\nType:TokenType.K_VOID\nParameters:\nParameter" \
                   ":\nName:x\nType:TokenType.K_INTEGER\nRefer:True\nInstructions:\nAssign:\nLeft assign " \
                   "operand:\nVariable:\nx\nRight assign operand:\nAdd:\nLeft add operand:\nVariable:\nx\nRight add " \
                   "operand:\nInteger:\n1}"

        self.assertEqual(par, expected)


if __name__ == '__main__':
    unittest.main()
