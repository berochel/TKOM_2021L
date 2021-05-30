#    Written by: Jarosław Zabuski, 2021

from argparse import ArgumentParser

from my_parser.parser import Parser

import my_interpreter.lib_methods as lib
from lexer.source_read import TextSource
from my_interpreter.visitor import Visitor, Interpreter

if __name__ == '__main__':
    arg_parser = ArgumentParser()

    arg_parser.add_argument('--file_path', type=str, default='../test_files/test_interpreter_code.txt')
    arg_parser.add_argument('--ident_length', type=int, default=64)
    arg_parser.add_argument('--string_length', type=int, default=256)

    args = arg_parser.parse_args()

    textSource = TextSource(args.file_path)

    parser = Parser(args.ident_length, args.string_length, textSource)

    tree = parser.parse()

    visitor = Visitor(tree)

    program = Interpreter(visitor, lib)

    program.interpret()

    print(f'Returned {program.return_val}.')
