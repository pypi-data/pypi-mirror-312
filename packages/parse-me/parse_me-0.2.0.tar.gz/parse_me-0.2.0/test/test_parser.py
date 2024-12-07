import unittest
from parse_me.parse import _parse_name, parse_tsv


class TestParsing(unittest.TestCase):
    def test_name_arabic(self):
        name = "عبد المسيح بن عبد الله ابن ناعمة الحمصي"
        parts = {"ISM": "عبد المسيح", "IAB": "عبد الله", "IAM": "ناعمة", "NSB": "الحمصي"}
        self.assertEqual(parts, _parse_name(name))

    def test_file_arabic(self):
        res = parse_tsv("test_arabic.tsv", "name", "ar")
        self.assertEqual("test_arabic_parsed.tsv", res)

    def test_Usaybiah(self):
        res = parse_tsv("UsaybiePeople.txt", "original", "arL")
        self.assertEqual("UsaybiePeople.txt_parsed.tsv", res)

    def test_Laski(self):
        res = parse_tsv("LASKI.tsv", "title", "en")
        self.assertEqual("LASKI.tsv_parsed.tsv", res)

    def test_Zylbercweig(self):
        res = parse_tsv("Zylbercweig2.tsv", "title", "he", "description")
        self.assertEqual("Zylbercweig2.tsv_parsed.tsv", res)

    def test_Majlis(self):
        res = parse_tsv("Majlis_AR.tsv", "title", "arL")
        self.assertEqual("Majlis_AR.tsv_parsed.tsv", res)



if __name__ == '__main__':
    unittest.main()
