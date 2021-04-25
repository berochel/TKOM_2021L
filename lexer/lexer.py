#    Written by: Jarosław Zabuski, 2021

import string

from error.error_handlers import LexerError
from lexer.token import Position, new_token, move_forward
from lexer.types import TokenType, token_type_repr


# Main lexer class, containing all methods needed to generate a valid
# lexical tokens tree from a source text. InputLexer and FileLexer
# classes are used as a source text handlers, generalising and simplyfying
# file processing.
class LexerMain:
    def __init__(self, maxIdentLength, maxStringLength, textSource=None):

        self.maxIdentLength = maxIdentLength
        self.maxStringLength = maxStringLength
        self.textSource = textSource

        self.readCursorPosition = Position(row=1, column=-1)
        self.start = Position(row=1, column=-1)

        self.token = new_token(TokenType.UNKNOWN, 0, Position(1, 0), Position(1, 0))
        self.tokenValue = ''
        self.current_char = ''

        self.get_next_char()

    def get_next_char(self):

        if not self.textSource.is_end_of_text():
            self.current_char = self.textSource.read_char()

            readCursorPosition = self.readCursorPosition
            readCursorPosition = move_forward(self.current_char, readCursorPosition.column, readCursorPosition.row, )
            self.readCursorPosition = readCursorPosition

    def is_eot_token(self):
        return self.token.type == TokenType.EOT

    def get_token(self):

        self.tokenValue = ''

        self.skip_whitespaces()

        self.start = self.readCursorPosition

        self.generate_unknown_token_placeholder()

        self.generate_eot_token()

        self.generate_comment_token()

        self.generate_string_token()

        self.generate_keyword_or_ident_token()

        self.generate_integer_or_double_token()

        self.generate_special_char_or_unknown_token()

        if self.token.type == TokenType.UNKNOWN:
            raise LexerError(self.token.value, self.token.end, "")

        return self.token

    def skip_whitespaces(self):

        while str(self.current_char) in string.whitespace and not self.textSource.is_end_of_text():
            self.get_next_char()

    def generate_unknown_token_placeholder(self):

        self.token = new_token(TokenType.UNKNOWN, 0, Position(1, 0), Position(1, 0))
        return self.token

    def generate_eot_token(self):

        if self.textSource.is_end_of_text():
            self.token = new_token(TokenType.EOT, self.tokenValue, self.readCursorPosition, self.readCursorPosition)
            return self.token

    def generate_comment_token(self):

        # checks if first char is "/"
        if self.current_char != '/':
            return None

        self.get_next_char()
        # checks if second char is "/". returns TokenType.DIV if not.
        if self.current_char != '/':

            self.token = new_token(TokenType.DIV, self.tokenValue, self.start)

        else:
            # second char is "/". Returns valid VALUE_COMMENT token, generated from // chars to end of line.
            self.get_next_char()

            while self.current_char != '\n':
                self.tokenValue += self.current_char
                self.get_next_char()

            self.token = new_token(TokenType.VALUE_COMMENT, self.tokenValue, self.start)

        return self.token

    def generate_string_token(self):

        # checks if first char is """
        if self.current_char != '\"':
            return None

        self.get_next_char()
        stringLength = self.maxStringLength

        # gets all chars until second, unescaped quote char appears
        while self.current_char != '\"' and stringLength > 0:

            # escapes quote char or anything else, if needed. Doesnt write slash char to
            # the string value.
            if self.current_char == "\\":
                self.get_next_char()

            self.tokenValue += self.current_char
            self.get_next_char()

            stringLength -= 1

        # Encountered a string that exceeds max allowed length. Raises an error.
        if stringLength <= 0:
            stop = self.readCursorPosition
            raise LexerError(self.current_char, stop, " (Exceeded maximum length of a string literal)")

        # escapes second quote char
        self.get_next_char()

        self.token = new_token(TokenType.VALUE_STRING, self.tokenValue, self.start)

        return self.token

    def generate_keyword_or_ident_token(self):

        # checks if current char signifies that a keyword or ident appears.
        if not self.current_char.isalpha() and self.current_char != '_':
            return None

        identLength = self.maxIdentLength

        # gets all valid chars until max length is reached and value is cut short
        while (self.current_char.isalnum() or self.current_char == '_') and identLength > 0:
            self.tokenValue += self.current_char
            self.get_next_char()
            identLength -= 1

        # Encountered an identifier that exceeds max allowed length. Raises an error.
        if identLength <= 0:
            stop = self.readCursorPosition
            raise LexerError(self.current_char, stop, " (Exceeded maximum length of a identifier literal)")

        # checks whether or not token might be a keyword or not
        key = token_type_repr.get(self.tokenValue)

        if key:
            self.token = new_token(key, self.tokenValue, self.start)
        else:
            self.token = new_token(TokenType.VALUE_ID, self.tokenValue, self.start)

        return self.token

    def generate_integer_or_double_token(self):

        # checks if current character is a valid digit
        if not self.current_char.isdigit():
            return None
        elif self.current_char == "0":
            self.generate_zero_integer_token()
        else:
            self.generate_nonzero_integer_token()

        return self.token

    def generate_nonzero_integer_token(self):

        # Non zero digit: takes all valid digits and checks, if there is
        # a dot char. If there is, parses double value. If not, just returns
        # the number.
        numberTokenValue = 0

        # gets all valid characters and represents them as an integer value.
        # creates integer part of a number.
        while self.current_char.isdigit():
            numberTokenValue = numberTokenValue * 10 + int(self.current_char)
            self.get_next_char()

        # checks if character is meant to be a double.
        if self.current_char == ".":
            self.generate_double_token(numberTokenValue)
        else:
            self.token = new_token(TokenType.VALUE_INT, numberTokenValue, self.start)

        self.tokenValue = str(numberTokenValue)

    def generate_zero_integer_token(self):

        # Zero digit char: checks if there is a dot char. If not and there is
        # a digit instead, raises Lexical Error. If not and there is
        # another char, returns 0 as Integer. If yes, parses double
        # value.
        numberTokenValue = 0
        self.tokenValue = '0'

        self.get_next_char()

        if self.current_char == ".":
            self.generate_double_token(numberTokenValue)

        elif self.current_char.isdigit():
            stop = self.readCursorPosition
            raise LexerError(self.tokenValue, stop, "")

        else:
            self.token = new_token(TokenType.VALUE_INT, numberTokenValue, self.start)

    def generate_double_token(self, numberTokenValue):

        # creates appropiate denominator and decimal part of newly parsed
        # double value.
        decimalTokenValue = 0
        decimalDenominator = 0
        self.get_next_char()

        while self.current_char.isdigit():
            decimalTokenValue = decimalTokenValue * 10 + int(self.current_char)
            decimalDenominator += 1
            self.get_next_char()

        self.token = new_token(TokenType.VALUE_DOUBLE, numberTokenValue, self.start, decimalTokenValue,
                               decimalDenominator)

    def generate_special_char_or_unknown_token(self):

        # checks if any ALNUM token or EOT token was evaluated before. Ensures that
        # single special chars are evaluated properly.
        if self.tokenValue.isalnum() or self.token.type == TokenType.EOT:
            return None

        self.tokenValue += self.current_char

        # Generates single special char token and reads next char for processing
        # during next get_token call.
        key = token_type_repr.get(self.tokenValue)
        if key:
            self.get_next_char()
            self.token = new_token(key, self.tokenValue, self.start)

        return self.token
