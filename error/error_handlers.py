from lexer.token import Position


class LexerError(Exception):
    def __init__(self, illegal_char, position: Position, additional_msg):
        self.illegal_char = illegal_char
        self.position = position
        self.message = f'Unable to recognize: "{self.illegal_char}" at: {self.position.print_location()}' \
                       + additional_msg
        super().__init__(self.message)


class ParserError(Exception):
    def __init__(self, illegal_token, position: Position, additional_msg):
        self.illegal_token = illegal_token
        self.position = position
        self.message = f'Unexpected: "{self.illegal_token}" at: {self.position.print_location()}' \
                       + additional_msg
        super().__init__(self.message)


class MainNotDeclaredError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class NotTheSameTypesError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class IncorrectArgumentsNumberError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class InvalidInitialisationError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class UndeclaredSymbol(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class NoParentContextError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class OverwriteError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class UndeclaredMethod(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class InvalidCall(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class ZeroDivisionError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
