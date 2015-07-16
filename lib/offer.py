__author__ = 'Petter'

class Offer:
    def __init__(self, actor, commodity_id, quantity, price=None):
        self.actor = actor
        self.commodity_id = commodity_id
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return "<Offer:%X %s x %s @ %s>" % (self.actor.id, self.commodity_id, self.quantity, self.price)


