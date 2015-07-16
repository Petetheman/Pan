__author__ = 'Petter'
from random import uniform
class Belief():
    def __init__(self, lower, upper):
        self.upper = upper
        self.lower = lower

    def mean(self):
        return (self.upper+self.lower)/2

    def width(self):
        return (self.upper-self.lower)

    def move(self, market_price):
        delta = self.mean()-market_price
        self.upper -= delta/2
        self.lower -= delta/2

    def narrow(self, adaption_rate = 0.05):
        mean = self.mean()
        self.lower += mean*adaption_rate
        self.upper -= mean*adaption_rate

    def widen(self, adaption_rate = 0.05):
        mean = self.mean()
        self.lower -= mean*adaption_rate
        self.upper += mean*adaption_rate

    def random(self):
        return uniform(self.lower, self.upper)

    def to_list(self):
        return [self.lower, self.upper]

    def __repr__(self):
        str = "<Belief %r..%r>" % (self.lower, self.upper)
        return str