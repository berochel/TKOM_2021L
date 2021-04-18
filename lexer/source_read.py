#    Written by: Jarosław Zabuski, 2021

# Contains basic file access class and methods.

class TextSource:
    def read_line(self):

        pass

    def is_end_of_text(self):

        pass


class TextSourceFromFile(TextSource):
    def __init__(self, path):

        self.fs = open(path, 'r')
        self.eof = False

    def read_line(self):

        line = self.fs.readline()
        if not line:
            self.eof = True
        return line

    def is_end_of_text(self):

        return self.eof

    def __del__(self):

        self.fs.close()


class TextSourceFromInput(TextSource):
    def __init__(self):

        self.text = None

    def read_line(self):

        self.text = input('>> ')
        return self.text

    def is_end_of_text(self):

        return self.text == 'DONE'
