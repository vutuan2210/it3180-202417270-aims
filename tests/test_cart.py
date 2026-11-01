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

    def test_total_cost_with_discount(self):
        cart = Cart()
        cart.add_dvd(DigitalVideoDisc("Disc", cost=100.0))
        self.assertAlmostEqual(cart.total_cost_with_discount(20), 80.0)

    def test_discount_percent_out_of_range(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.total_cost_with_discount(150)


if __name__ == "__main__":
    unittest.main()
