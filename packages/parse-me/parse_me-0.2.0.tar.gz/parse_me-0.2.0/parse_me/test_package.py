import unittest
from parse_me.parse import get_supported_languages, parse_name, parse_tsv
from parse_me.name_parsing_prompts import LANGS
import os

class TestInterfaces(unittest.TestCase):
    def test_get_langs(self):
        """
        Test the get_langs function, make sure the returned type is a dict and the number of keys match the number
        of languages in LANGS and that a non-empty string is returned for each value of the dictionary
        :return:
        """
        langs = get_supported_languages()
        self.assertIsInstance(langs, dict)
        self.assertEqual(len(langs), len(LANGS))
        for lang in langs.values():
            self.assertIsInstance(lang, str)
            self.assertTrue(len(lang) > 0)

    def test_parse_name(self):
        """
        Test the parse_name function, make sure the returned type is a dict and the keys are the expected ones
        :return:
        """
        res = parse_name("عبد المسيح بن عبد الله ابن ناعمة الحمصي", "ar")
        self.assertIsInstance(res, dict)
        self.assertSetEqual(set(res.keys()), {'nisba', 'matronymic', 'patronymic', 'given-name', 'explanations'})

    def test_parse_tsv(self):
        """
        Test the parse_tsv function, make sure the returned type is a string and that the file exists
        :return:
        """
        res = parse_tsv("sample.tsv", "title", "heL", "description", model_name='claude-3-5-haiku-20241022')
        self.assertIsInstance(res, str)
        self.assertTrue(os.path.exists(res))
if __name__ == '__main__':
    unittest.main()
