#    Written by: Jarosław Zabuski, 2021

# Parses runtime arguments, like type of file input and file path
# (if text input is selected to be a file) and runs appropiate
# Lexer text input handlers to run the process of tokenization.

from argparse import ArgumentParser

from my_parser.parser import Parser
from objbrowser import browse

from lexer.source_read import TextSource

if __name__ == '__main__':
    arg_parser = ArgumentParser()

    arg_parser.add_argument('--file_path', type=str, default='../test_files/test_code.txt')
    arg_parser.add_argument('--ident_length', type=int, default=64)
    arg_parser.add_argument('--string_length', type=int, default=256)

    args = arg_parser.parse_args()

    textSource = TextSource(args.file_path)

    parser = Parser(args.ident_length, args.string_length, textSource)

    program = parser.parse()

    browse(program)
