import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_title


class TestSearchByTitle(unittest.TestCase):
    def setUp(self):
        self.items = [
            DigitalVideoDisc("The Lion King"),
            DigitalVideoDisc("Star Wars"),
        ]

    def test_exact_case(self):
        self.assertEqual([d.title for d in search_by_title(self.items, "Lion")], ["The Lion King"])

    def test_ignores_case(self):
        self.assertEqual([d.title for d in search_by_title(self.items, "lion")], ["The Lion King"])


if __name__ == "__main__":
    unittest.main()
