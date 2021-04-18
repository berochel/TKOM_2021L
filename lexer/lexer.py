#    Written by: Jarosław Zabuski, 2021

# Contains all main tokenization methods and Lexer inplementations.

import argparse

from lexer.token.token import Token, Position, new_token
from lexer.token.types import TokenType
from lexer.token.regex_rules import compile_regex
from lexer.source_read import TextSourceFromFile, TextSourceFromInput
from error.error_handlers import LexerError


# Main lexer class, containing all methods needed to generate a valid
# lexical token tree from a source text. InputLexer and FileLexer
# classes are used as a source text handlers, generalising and simplyfying
# file processing.
class LexerMain:
    def __init__(self, textSource=None):

        self.textSource = textSource
        self.readCursorPosition = Position(row=1, column=0)
        self.regexTable = compile_regex()
        self.tokens = None
        self.token_iter = 0

    # Iterates through the table of all generated tokens and returns
    # the same token that was returned in the last call to this
    # function if move_index is false, or the next one in line
    # , if it's true.
    def get_next_token(self, move_index=True):

        if self.token_iter < len(self.tokens):
            token = self.tokens[self.token_iter]
            if move_index:
                self.token_iter += 1
            return token
        return None

    # Checks if the token iterator is in bounds. True, if there are tokens
    # to process, or false otherwise.
    def if_next_token_valid(self):

        return True if self.token_iter < len(self.tokens) else False

    # Processes lines of source text in loop, gathering tokens from next line
    # of text if possible, and appending them to the main table of all found
    # tokens.
    def get_tokens_from_source(self):

        all_tokens = []
        while not self.textSource.is_end_of_text():

            tokens = self.get_tokens_from_line()
            all_tokens.extend(tokens)

        return all_tokens

    # Processes a single line of source text. Responsible for reading a new line of text from
    # source text and keeping track of read cursor position in rows.
    def get_tokens_from_line(self):

        line = self.textSource.read_line()
        tokens = self.get_tokens_from_specified_line(line)
        self.readCursorPosition.row += 1

        return tokens

    # Processes a single line of source text. Used during tests to inject
    # test examples.
    def get_tokens_from_specified_line(self,line):

        if line:
            tokens = self.line_lex(line)
        else:
            tokens = [Token(TokenType.T_EOT, self.readCursorPosition.copy(), self.readCursorPosition.copy())]

        return tokens

    # Responsible for keeping track of read cursor position in columns, invoking main token
    # generation in valid bounds of line, and updating token table (and skipping ignorable
    # tokens, like whitespaces and comments). Here we also take care of specific operations
    # such as splicing a single string literal token created by regex rules, into three
    # separate tokens, to account for single quote character escaping and for
    # readability reasons.
    def line_lex(self, line):

        self.readCursorPosition.column = 0
        tokens = []
        while self.readCursorPosition.column < len(line):
            token = self.get_single_token(line)

            if token.type is not TokenType.T_IGNORE:

                if token.type is TokenType.VT_STRING:

                    tempToken = new_token(TokenType.T_QUOTE, token.value, token.start, token.start + 1)
                    tokens.append(tempToken)
                    tempToken = new_token(TokenType.VT_STRING, token.value[1:-1], token.start + 1,
                                          token.end - 1)
                    tokens.append(tempToken)
                    tempToken = new_token(TokenType.T_QUOTE, token.value, token.end - 1, token.end)
                    tokens.append(tempToken)

                elif token.type is TokenType.T_COMMENT_SIGN:

                    tokens.append(token)
                    value = line[token.end.column:-1]
                    pos_start = Position(token.end.row, token.end.column)
                    pos_end = Position(token.end.row, len(line) - 1)
                    token = new_token(TokenType.VT_COMMENT, value, pos_start, pos_end)
                    tokens.append(token)

                else:
                    tokens.append(token)

            self.readCursorPosition.column = token.end.column

        return tokens

    # Responsible for proper lexer error handling, like, for example, unsupported characters
    # found in source text.
    def get_single_token(self, line):

        try:
            return self.find_single_token(line)
        except LexerError as e:
            e.print_error_and_exit()

    # Main token generation method: checks if any regex rules strike a match and produce
    # a valid token. Checks from left to right for valid tokens, and if matched, creates
    # a new token, updates its type, value ("if it has a value, for example, when processing
    # string literal or an identifier of a variable), and position in the source text.
    # Raises LexerError, if in any point a line has a character not meant to be used in source
    # code.
    def find_single_token(self, line):

        for regex in self.regexTable:
            match = regex.match(line, self.readCursorPosition.column)

            if match:

                token_type = self.regexTable[regex]
                value = match.group(0)
                pos_start = self.readCursorPosition.copy()
                pos_end = Position(self.readCursorPosition.row, match.end(0))
                matching_token = new_token(token_type, value, pos_start, pos_end)
                return matching_token

        raise LexerError(line[self.readCursorPosition.column], self.readCursorPosition)


# Supports LexerMain class with an easy way to generalize different
# text input handling methods. FileSource defined in source_read.py.
# Initializes main Lexer class and starts the process of tokenizing
# the source text.
class FileLexer(LexerMain):

    def __init__(self, file_path):

        super().__init__(textSource = TextSourceFromFile(file_path))
        self.tokens = self.get_tokens_from_source()


# Supports LexerMain class with an easy way to generalize different
# text input handling methods. InputSource defined in source_read.py.
# Initializes main Lexer class and starts the process of tokenizing
# the source text.
class InputLexer(LexerMain):

    def __init__(self):

        super().__init__(textSource = TextSourceFromInput())
        self.tokens = self.get_tokens_from_source()


# Parses runtime arguments, like type of file input and file path
# (if text input is selected to be a file) and runs appropiate
# Lexer text input handlers to run the process of tokenization.
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--verbose', '-v', action="store_true")
    parser.add_argument('--file_path', type = str, default = 'test_files/test_lexer.txt')
    parser.add_argument('--lexer_type', type = str, choices = ['stdin', 'file'], default = 'file')

    args = parser.parse_args()

    if args.lexer_type == 'stdin':
        lexer = InputLexer()
    else:
        lexer = FileLexer(args.file_path)

    while lexer.if_next_token_valid():

        if args.verbose:
            token = lexer.get_next_token()
            print(f'{token}  ,  token type: {token.type}  ,  {token.print_location()}')
        else:
            print(lexer.get_next_token())
