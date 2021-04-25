#    Written by: Jarosław Zabuski, 2021

# Contains basic file access class and methods.

class TextSource:
    def read_line(self):

        pass

    def is_end_of_text(self):

        pass


class TextSourceFromFile(TextSource):
    def __init__(self, path):

        self.eof = False
        self.text = ""
        self.line = ""

        with open(path) as fileObj:
            for line in fileObj:
                self.text += line

    def read_char(self):

        if self.text != "":
            char = self.text[0]
            self.text = self.text[1:]
            return char
        else:
            self.eof = True
            return ''

    def peek_next_char(self):

        return self.text[0]

    def is_end_of_text(self):

        return self.eof


class TextSourceFromInput(TextSource):

    def __init__(self):
        self.line = ""
        self.text = ""

        self.read_text()

    def read_line(self):
        self.line = input('>> ')
        return self.line

    def is_end_of_input(self):
        return self.line == 'DONE'

    def is_end_of_text(self):
        return self.text == 'DONE'

    def read_text(self):
        while not self.is_end_of_input():
            self.line = self.read_line()
            self.text += self.line

        self.text = self.text[:-4] + " " + self.text[-4:-1] + "E"

    def read_char(self):
        char = self.text[0]
        self.text = self.text[1:]

        return char

    def peek_next_char(self):
        return self.text[0]
