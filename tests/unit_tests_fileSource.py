#    Written by: Jarosław Zabuski, 2021

# Contains tests checking the actions performed by the FileSource class.

import unittest

from lexer.source_read import TextSourceFromFile

TEST_SOURCE_1_LINE = '../test_files/test_lexer_singleLineReadExample.txt'
TEST_SOURCE_2_LINES = '../test_files/test_lexer_twoLineReadExample.txt'


class TestSource(unittest.TestCase):

    def test_file_source(self):

        text = ""
        file_source = TextSourceFromFile(TEST_SOURCE_1_LINE)
        while not file_source.is_end_of_text():
            text += file_source.read_char()

        self.assertEqual("test Integer 5 Double 1;", text, msg='Error in first line.')
        self.assertEqual(True, file_source.is_end_of_text(), 'Error when checking EOF')

    def test_file_source_three_lines(self):

        text = ""
        file_source = TextSourceFromFile(TEST_SOURCE_2_LINES)
        while not file_source.is_end_of_text():
            text += file_source.read_char()

        self.assertEqual("test1 sampleId1\ntest2 sample_2", text, msg='Error in first line.')
        self.assertEqual(True, file_source.is_end_of_text(), msg='Error when checking EOF')


if __name__ == '__main__':
    unittest.main()
