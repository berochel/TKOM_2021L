#    Written by: Jarosław Zabuski, 2021

import unittest

from lexer.lexer import LexerMain


class TestSource(unittest.TestCase):

    def test_file_source(self):

        from lexer.source_read import TextSourceFromFile
        textSource = TextSourceFromFile('../test_files/test_lexer.txt')

        lexer = LexerMain(textSource=textSource, maxIdentLength=64)

        while not lexer.is_eot_token():

            if True:
                token = lexer.get_token()
                print(f'{token},  token type: {token.type},  {token.print_location()}')

        self.assertEqual(True, lexer.is_eot_token(), 'Error when checking EOF')

        token = lexer.get_token()
        print(f'{token},  token type: {token.type},  {token.print_location()}')

        self.assertEqual(True, lexer.is_eot_token(), 'Error when checking EOF')

        token = lexer.get_token()
        print(f'{token},  token type: {token.type},  {token.print_location()}')

        self.assertEqual(True, lexer.is_eot_token(), 'Error when checking EOF')

        token = lexer.get_token()
        print(f'{token},  token type: {token.type},  {token.print_location()}')

        self.assertEqual(True, lexer.is_eot_token(), 'Error when checking EOF')


if __name__ == '__main__':
    unittest.main()
