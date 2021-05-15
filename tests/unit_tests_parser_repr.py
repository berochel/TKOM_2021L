#    Written by: Jarosław Zabuski, 2021

import unittest

from my_parser.parser import Parser


class ParserTest(unittest.TestCase):

    def test_file_source(self):
        from lexer.source_read import TextSource
        textSource = TextSource('../test_files/test_parser_simple_function.txt')

        parser = Parser(64, 256, textSource)

        program = parser.parse()

        program_repr = program.__repr__()

        expected_repr = "Program:\nFunction:\nName:pow\nType:TokenType.K_VOID\nParameters:\nParameter:\nName:x\nType" \
                        ":TokenType.K_DOUBLE\nRefer:True\nInstructions:\nAssign:\nLeft assign " \
                        "operand:\nVariable:\nx\nRight assign operand:\nMul:\nLeft mul operand:\nVariable:\nx\nRight " \
                        "mul operand:\nVariable:\nx"

        self.assertEqual(program_repr, expected_repr)


if __name__ == '__main__':
    unittest.main()
