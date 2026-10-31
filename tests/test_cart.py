import unittest

from aims.cart import Cart, MAX_NUMBERS_ORDERED
from aims.dvd import DigitalVideoDisc


class TestCart(unittest.TestCase):
    def test_add_dvd_until_full(self):
        cart = Cart()
        for i in range(MAX_NUMBERS_ORDERED):
            self.assertTrue(cart.add_dvd(DigitalVideoDisc(f"Disc {i}", cost=1.0)))
        self.assertFalse(cart.add_dvd(DigitalVideoDisc("One too many", cost=1.0)))
        self.assertEqual(len(cart.items), MAX_NUMBERS_ORDERED)


if __name__ == "__main__":
    unittest.main()
