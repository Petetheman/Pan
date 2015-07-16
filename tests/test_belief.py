import unittest
from Pan.lib.belief import Belief
class TestBelief(unittest.TestCase):
    def setUp(self):
        self.lower = 4
        self.upper = 6
        self.signigicant_delta = 0.25
        self.adaptability = 0.05
        self.belief = Belief(self.lower,self.upper, self.signigicant_delta, self.adaptability)

    def test_mean(self):
        mean = self.belief.mean()
        self.assertEqual(mean, 5)

    def test_width(self):
        width = self.belief.width()
        self.assertEqual(width, 2)

    def test_move(self):
        self.belief.move(5.5)
        self.assertEqual(self.belief.mean(), 5.25)


    def test_narrow(self):
        self.belief.narrow()
        self.assertEqual(self.belief.width(), 1.5)
        self.assertEqual([self.belief.lower, self.belief.upper], [4.25, 5.75])


    def test_widen(self):
        self.belief.widen()
        self.assertEqual(self.belief.width(), 2.5)



