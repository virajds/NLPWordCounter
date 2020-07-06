import unittest

from wordCounter import count_words

class TestWordCount(unittest.TestCase):
    # Simple test without words
    def test_count_words_1(self):
        count_data = count_words(path=None,
                                    words=None,
                                    paragraph="Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                              "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                                              "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi "
                                              "ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit "
                                              "in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
                                              "sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
                                              "mollit anim id est laborum.")

        self.assertEqual(count_data[0][1], 2)
        self.assertEqual(count_data[0][0], "Dolor")

    # Simple test with words
    def test_count_words_2(self):
        count_data = count_words(path=None,
                                 words="veniam",
                                 paragraph="Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                           "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                                           "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi "
                                           "ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit "
                                           "in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
                                           "sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
                                           "mollit anim id est laborum.")

        self.assertEqual(count_data[0][1], 1)
        self.assertEqual(count_data[0][0], "Veniam")

    #Non ASCII test
    def test_count_words_3(self):
        count_data = count_words(path=None,
                                 words="⅞",
                                 paragraph="½⅓¼⅕⅙⅐⅛⅑ ⅔⅖ ¾⅗ ⅘ ⅚⅝ ⅞")

        self.assertEqual(count_data[0][1], 1)
        self.assertEqual(count_data[0][0], "⅞")

    # Full test with words
    def test_count_words_4(self):
        count_data = count_words(path="ExampleDocs/Test Docs/",
                                 words="Government",
                                 paragraph=None)

    # Full test without words
    def test_count_words_5(self):
        count_data = count_words(path="ExampleDocs/Test Docs/",
                                 words=None,
                                 paragraph=None)

if __name__ == '__main__':
    unittest.main()