from lexer.token import Position

class LexerError(Exception):
    def __init__(self, illegal_char, position: Position, additional_msg):
        self.illegal_char = illegal_char
        self.position = position
        self.message = f'Unable to recognize: "{self.illegal_char}" at: {self.position.print_location()}' + additional_msg
        super().__init__(self.message)
