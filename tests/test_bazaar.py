__author__ = 'Petter'
import unittest
from pprint import pprint

from lib.actor import Actor
from lib.bazaar import Bazaar
from Pan.lib.offer import Offer


class TestBazaar(unittest.TestCase):
    def setUp(self):
        self.commodities = {"A": {}, "B": {}, "C": {}, "AB": {"A":1, "B": 1}, "BC": {"B": 1, "C": 1}, "CA": {"C": 1, "A": 1}}
        self.actors = [Actor("A"), Actor("B")]
        self.bazaar = Bazaar(self.commodities, self.actors)

    def test_init(self):
        commodities = {"A": {}, "B": {}, "AB": {"A":1, "B": 1}}
        actors = [Actor("AB")]
        bazaar = Bazaar(commodities, actors)
        self.assertEqual(bazaar.commodity_count(), 3)
        self.assertEqual(bazaar.actor_count(), 1)

    def test_add_history(self):
        self.bazaar.add_history("price", "A", 1)
        self.assertEqual(self.bazaar.history["price"]["A"], [0.5,1.5,1])

    def test_avg_history(self):
        #Added by Market init function
        #self.bazaar.add_history("price", "A", 0.5)
        #self.bazaar.add_history("price", "A", 1.5)
        self.bazaar.add_history("price", "A", 2)
        self.bazaar.add_history("price", "A", 3)
        self.bazaar.add_history("price", "A", 4)

        result = self.bazaar.avg_history("price", "A", 1)
        self.assertEqual(result, 4)
        result = self.bazaar.avg_history("price", "A", 2)
        self.assertEqual(result, 3.5)
        result = self.bazaar.avg_history("price", "A", 3)
        self.assertEqual(result, 3)
        result = self.bazaar.avg_history("price", "A", 4)
        self.assertEqual(result, 2.625)
        result = self.bazaar.avg_history("price", "A", 5)
        self.assertEqual(result, 2.2)
        result = self.bazaar.avg_history("price", "A", 6)
        self.assertEqual(result, 2.2)

    def test_set_history(self):
        self.bazaar.set_history("price", "A", [9,9,9,9,9,9])
        self.assertEqual([9,9,9,9,9,9], self.bazaar.get_history("price","A"))

    def test_resolve_offers_A(self):
        o_ask = Offer(self.actors[0], "A", 1, 10)
        o_bid = Offer(self.actors[1], "A", 1, 10)

        self.bazaar.ask(o_ask)
        self.bazaar.bid(o_bid)

        self.bazaar.resolve_offers("A")

        self.assertEqual(self.actors[0].get_inventory("A"), -1)
        self.assertEqual(self.actors[0].get_money(), 1010)
        self.assertEqual(self.actors[1].get_money(), 990)
        self.assertEqual(self.actors[1].get_inventory("A"), 1)

    def test_resolve_offers_B(self):
        o_ask = Offer(self.actors[0], "A", 1, 5)
        o_bid = Offer(self.actors[1], "A", 1, 10)

        self.bazaar.ask(o_ask)
        self.bazaar.bid(o_bid)

        self.bazaar.resolve_offers("A")

        self.assertEqual(self.actors[0].get_inventory("A"), -1)
        self.assertEqual(self.actors[0].get_money(), 1007.5)
        self.assertEqual(self.actors[1].get_money(), 992.5)
        self.assertEqual(self.actors[1].get_inventory("A"), 1)

    def test_simulate(self):
        commodities = {"A": {}, "B": {}, "C": {}, "AB": {"A":1, "B": 1}, "BC": {"B": 1, "C": 1}, "CA": {"C": 1, "A": 1}, "ABBC": {"AB": 1, "BC": 1}, "BCCA": {"BC": 1, "CA": 1}, "CAAB": {"CA":1,"AB":1}}
        actors = [Actor("A"),Actor("A"),Actor("A"), Actor("B"), Actor("B"), Actor("B"), Actor("C"), Actor("C"), Actor("C"), Actor("AB"), Actor("AB"), Actor("AB"), Actor("BC"), Actor("BC"), Actor("BC"), Actor("CA"), Actor("CA"), Actor("CA"), Actor("ABBC"), Actor("ABBC"), Actor("ABBC"), Actor("BCCA"), Actor("BCCA"), Actor("BCCA"), Actor("CAAB"), Actor("CAAB"), Actor("CAAB")]
        bazaar = Bazaar(commodities, actors)
        bazaar.simulate(2000)
        pprint(bazaar.__dict__, None, 1, 200,)
        pprint(actors[9].__dict__, None, 1, 200,)
        pprint(bazaar.avg_history("price", "A",1))
        bazaar.simulate(1)
        pprint(actors[9].inventory.get_space_empty(), None, 1, 200,)
        pprint(actors[9].get_belief("A"), None, 1, 200,)
        pprint(actors[9].get_inventory("A"), None, 1, 200,)
        pprint(actors[9].determine_buy_quantity(bazaar, "A"), None, 1, 200,)
        bazaar.simulate(1)
        pprint(actors[9].inventory.get_space_empty(), None, 1, 200,)
        pprint(actors[9].get_belief("A"), None, 1, 200,)
        pprint(actors[9].get_inventory("A"), None, 1, 200,)
        pprint(actors[9].determine_buy_quantity(bazaar, "A"), None, 1, 200,)
        bazaar.simulate(1)
        pprint(actors[9].inventory.get_space_empty(), None, 1, 200,)
        pprint(actors[9].get_belief("A"), None, 1, 200,)
        pprint(actors[9].get_inventory("A"), None, 1, 200,)
        pprint(actors[9].determine_buy_quantity(bazaar, "A"), None, 1, 200,)


        #pprint(bazaar.actors[1].get_belief("A"), None, 1, 200,)
