__author__ = 'Petter'
import unittest

from Pan.lib.actor import Actor
from lib.bazaar import Bazaar


class TestActor(unittest.TestCase):
    def setUp(self):
        self.commodities = {"A": {}, "B": {}, "AB": {"A":1, "B": 1}}
        self.actor = Actor("AB")
        self.bazaar = Bazaar(self.commodities, [self.actor])

    def test_init(self):
        self.assertEqual([0.5,1.5], self.actor.get_belief("A"))
        self.assertEqual([0.5,1.5], self.actor.get_belief("B"))
        self.assertEqual([1.5,4.5], self.actor.get_belief("AB"))

        self.assertEqual([0.5,1.5], self.actor.get_clearing_price("A"))
        self.assertEqual([0.5,1.5], self.actor.get_clearing_price("B"))
        self.assertEqual([1.5,4.5], self.actor.get_clearing_price("AB"))

    def test_get_price_belief(self):
        price = self.actor.get_belief("A")
        self.assertEqual([0.5, 1.5], price)

    def test_update_price_belief(self):
        #Widen 0.05 of distance to market_mean and Move half of distance to market mean
        self.bazaar.set_history("price", "A", [8,8,8,8,8])
        belief = self.actor.set_belief("A", [3.5,4.5])
        self.actor.update_belief(self.bazaar, "sell", "A", False, 2)
        belief = self.actor.get_belief("A")
        self.assertEqual([5.3, 6.7], belief)

    def test_get_clearing_favorability(self):
        result = self.actor.get_clearing_favorability(0,0,10)
        self.assertEqual(0, result)
        result = self.actor.get_clearing_favorability(10,0,10)
        self.assertEqual(1, result)
        result = self.actor.get_clearing_favorability(5,0,10)
        self.assertEqual(0.5, result)

    def test_determine_sale_quantity(self):
        self.actor.inventory.set_quantity("A", 10)
        self.actor.inventory.set_ideal_quantity("A", 5)

        self.actor.set_clearing_price("A", [1,10])
        self.bazaar.set_history("price", "A", [10]*15)

        self.assertEqual(5, self.actor.determine_sale_quantity(self.bazaar, "A"))
        self.assertEqual(0, self.actor.determine_buy_quantity(self.bazaar, "A"))

    def test_determine_buy_quantity(self):
        self.actor.inventory.set_quantity("A", 5)
        self.actor.inventory.set_ideal_quantity("A", 10)

        self.actor.set_clearing_price("A", [1,10])
        self.bazaar.set_history("price", "A", [1]*15)

        self.assertEqual(5, self.actor.determine_buy_quantity(self.bazaar, "A"))
        self.assertEqual(0, self.actor.determine_sale_quantity(self.bazaar, "A"))

    def test_determine_buy_sale_quantity_medium_market(self):
        self.actor.inventory.set_quantity("A", 5)
        self.actor.inventory.set_ideal_quantity("A", 10)
        self.actor.set_clearing_price("A", [3,5])

        self.actor.inventory.set_quantity("B", 10)
        self.actor.inventory.set_ideal_quantity("B", 5)
        self.actor.set_clearing_price("B", [3,5])
        self.bazaar.set_history("price", "A", [4]*15)
        self.bazaar.set_history("price", "B", [4]*15)

        self.assertEqual(2.5, self.actor.determine_buy_quantity(self.bazaar, "A"))
        self.assertEqual(0, self.actor.determine_sale_quantity(self.bazaar, "A"))

        self.assertEqual(0, self.actor.determine_buy_quantity(self.bazaar, "B"))
        self.assertEqual(2.5, self.actor.determine_sale_quantity(self.bazaar, "B"))

    def test_generate_orders(self):
        self.actor.inventory.set_quantity("A", 5)
        self.actor.inventory.set_ideal_quantity("A", 10)

        self.actor.set_clearing_price("A", [1,10])
        self.bazaar.set_history("price", "A", [5]*15)

        self.actor.generate_offers(self.bazaar, "A")

        offer = self.bazaar.offers["A"]["bid"][0]

        self.assertAlmostEqual(len(self.bazaar.offers["A"]["bid"]), 1)
        self.assertAlmostEqual(offer.quantity, 2.777777777777777)
        self.assertAlmostEqual(offer.commodity_id, "A")
