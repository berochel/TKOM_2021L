#    Written by: Jarosław Zabuski, 2021

# Contains tests checking the actions performed by the FileSource class.

import unittest

from lexer.source_read import TextSourceFromFile

TEST_SOURCE_1_LINE = '../test_files/test_lexer_singleLineReadExample.txt'
TEST_SOURCE_2_LINES = '../test_files/test_lexer_twoLineReadExample.txt'


class TestSource(unittest.TestCase):

    def test_file_source(self):

        file_source = TextSourceFromFile(TEST_SOURCE_1_LINE)
        text = file_source.read_line()
        self.assertEqual("test Integer 5 Double 1;", text, msg='Error in first line.')
        file_source.read_line()
        self.assertEqual(True, file_source.is_end_of_text(), 'Error when checking EOF')

    def test_file_source_three_lines(self):

        file_source = TextSourceFromFile(TEST_SOURCE_2_LINES)
        text = file_source.read_line()
        self.assertEqual("test1 sampleId1\n", text, msg='Error in first line.')
        text = file_source.read_line()
        self.assertEqual("test2 sample_2", text, msg='Error in second line.')
        file_source.read_line()
        self.assertEqual(True, file_source.is_end_of_text(), msg='Error when checking EOF')


if __name__ == '__main__':
    unittest.main()
