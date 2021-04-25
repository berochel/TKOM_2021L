#    Written by: Jarosław Zabuski, 2021

# Parses runtime arguments, like type of file input and file path
# (if text input is selected to be a file) and runs appropiate
# Lexer text input handlers to run the process of tokenization.

from argparse import ArgumentParser

from lexer.lexer import LexerMain
from lexer.source_read import TextSourceFromInput, TextSourceFromFile

if __name__ == '__main__':

    parser = ArgumentParser()

    parser.add_argument('--verbose', '-v', action="store_true")
    parser.add_argument('--file_path', type=str, default='test_files/test_lexer.txt')
    parser.add_argument('--input_type', type=str, choices=['stdin', 'file'], default='file')
    parser.add_argument('--ident_length', type=int, default=64)

    args = parser.parse_args()

    if args.input_type == 'stdin':
        textSource = TextSourceFromInput()
    else:
        textSource = TextSourceFromFile(args.file_path)

    lexer = LexerMain(textSource=textSource, maxIdentLength=args.ident_length)

    while not lexer.is_eot_token():

        if args.verbose:
            token = lexer.get_token()
            print(f'{token},  token type: {token.type},  {token.print_location()}')
        else:
            print(lexer.get_token())
