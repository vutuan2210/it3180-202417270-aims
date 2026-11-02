import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_category


class TestSearchByCategory(unittest.TestCase):
    def setUp(self):
        self.items = [
            DigitalVideoDisc("The Lion King", "Animation"),
            DigitalVideoDisc("Star Wars", "Science Fiction"),
            DigitalVideoDisc("Aladdin", "Animation"),
        ]

    def test_finds_all_in_category(self):
        titles = [d.title for d in search_by_category(self.items, "Animation")]
        self.assertEqual(titles, ["The Lion King", "Aladdin"])

    def test_category_is_case_insensitive(self):
        self.assertEqual(len(search_by_category(self.items, "animation")), 2)

    def test_unknown_category(self):
        self.assertEqual(search_by_category(self.items, "Horror"), [])


if __name__ == "__main__":
    unittest.main()
