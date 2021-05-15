#    Written by: Jarosław Zabuski, 2021

# Contains basic file access class and methods.

class TextSource:
    def __init__(self, path):

        self.eof = False
        self.text = ""
        self.line = ""
        self.file = open(path, 'r')
        self._is_testing = False

        self.text = self.file.read(1)

    def __del__(self):
        self.file.close()

    def read_char(self):

        if self.text != "" and not self._is_testing:
            char = self.text
            self.text = self.file.read(1)
            return char
        elif self._is_testing:
            char = self.text[0]
            self.text = self.text[1:]
            return char
        else:
            self.eof = True
            return ''

    def is_end_of_text(self):
        if self._is_testing:
            return len(self.text) == 0

        return self.eof
