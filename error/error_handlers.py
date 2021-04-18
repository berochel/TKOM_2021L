import functools

from lexer.token.token import Position


def run_with_exception_safety(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except (LexerError) as e:
            e.print_error_and_exit()
        return result

    return wrapper


class LexerError(Exception):
    def __init__(self, illegal_char, position: Position):
        self.illegal_char = illegal_char
        self.position = position

    def print_error_and_exit(self):
        print(f'UnexpectedCharacterError: unable to recognize {self.illegal_char} at: {self.position.print_location()}')
        exit()
