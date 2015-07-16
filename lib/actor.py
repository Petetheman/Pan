__author__ = 'Petter'
from random import uniform

from lib.inventory import Inventory
from Pan.lib.offer import Offer


class Actor():
    SIGNIFICANT = 0.25
    SIGN_IMBALANCE = 0.33
    INVENTORY_LOW = 0.1
    INVENTORY_HIGH = 2.0
    PRICE_MIN = 0.01

    def __init__(self, labor_id = None):
        self.id = id(self)
        self.labor_id = labor_id
        self.alive = True

        self.money = 2000
        self.money_last = 2000
        self.profit = 0

        self.clearing_prices = {}
        self.price_beliefs = {}
        self.lookback = 15

        self.inventory = Inventory()

    def destroy(self):
        pass

    def init(self, bazaar):
        commodities = bazaar.commodities
        for commodity in commodities:
            trades = []
            price = bazaar.avg_history("price", commodity, self.lookback)
            trades.append(price*0.5)
            trades.append(price*1.5)

            self.clearing_prices[commodity] = list(trades)
            self.price_beliefs[commodity] = list(trades)




    #Logic Functions

    def produce(self, bazaar):
        #If no labor
        #   start best
        #   set ideal quantities
        #
        #if not ingredients
        #   is availiable on market?
        #       no? labor = None
        #
        #
        #if has ingredients
        #   remove them from inventory
        #   insert produced to inventory
        #   set no labor
        #   remove ideal quantities
        #self.labor_id = bazaar.get_most_profitable_labor(self.lookback)
        for k,v in bazaar.commodities[self.labor_id].items():
            self.inventory.set_ideal_quantity(k, v*5)

        recipe = bazaar.commodities[self.labor_id]
        if self.inventory.contains(recipe):
            for commodity_id, n in recipe.items():
                self.inventory.change_quantity(commodity_id, -n)
            self.inventory.change_quantity(self.labor_id, 1)






    def determine_price(self, commodity_id):
        return uniform(*self.get_belief(commodity_id))

    def determine_sale_quantity(self, bazaar, commodity_id):
        mean = bazaar.avg_history("price", commodity_id, self.lookback)
        range = self.get_clearing_price_range(commodity_id)
        favorability = self.get_clearing_favorability(mean,*range)
        quantity_to_sell = favorability * self.inventory.surplus(commodity_id)
        return quantity_to_sell

    def determine_buy_quantity(self, bazaar, commodity_id):
        mean = bazaar.avg_history("price", commodity_id, self.lookback)
        range = self.get_clearing_price_range(commodity_id)
        favorability = 1- self.get_clearing_favorability(mean,*range)
        quantity_to_sell = favorability * self.inventory.shortage(commodity_id)
        return quantity_to_sell




    def update_belief(self, bazaar, act, commodity_id, success, price=None):
        public_mean_price = bazaar.get_history("price", commodity_id,1)
        belief = self.get_belief(commodity_id)
        mean = (belief[0]+belief[1])/2
        delta = mean-public_mean_price

        if success:
            self.add_clearing_price(commodity_id, price)

            if act == "buy" and delta > Actor.SIGNIFICANT:
                self.move_belief(commodity_id, delta)
            elif act == "sell" and delta < -Actor.SIGNIFICANT:
                self.move_belief(commodity_id, delta)
            self.narrow_belief(commodity_id, mean)
        else:
            self.move_belief(commodity_id, delta)
            self.widen_belief(commodity_id, delta)

    def set_belief(self, commodity_id, belief):
        self.price_beliefs[commodity_id] = belief
        return belief

    def get_belief(self, commodity_id):
        return self.price_beliefs[commodity_id]

    def widen_belief(self, commodity_id, mean, wobble=0.05):
        belief = self.get_belief(commodity_id)
        belief[0] -= mean*wobble
        belief[1] += mean*wobble

        if belief[0]<=0:
            belief[0] = 0.01
        if belief[1] <= belief[0]:
            belief[1] = belief[0]+0.01
        return True

    def narrow_belief(self, commodity_id, mean, wobble=0.05):
        belief = self.get_belief(commodity_id)
        belief[0] += mean*wobble
        belief[1] -= mean*wobble
        if belief[1] <= belief[0]:
            belief[1] = belief[0]+0.01
        return True

    def move_belief(self, commodity_id, delta_mean_to_market):
        belief = self.get_belief(commodity_id)
        belief[0] -= delta_mean_to_market/2
        belief[1] -= delta_mean_to_market/2
        if belief[0]<=0:
            belief[0] = 0.01
        if belief[1] <= belief[0]:
            belief[1] = belief[0]+0.01
        return True





    def get_clearing_price(self, commodity_id):
        return self.clearing_prices[commodity_id]

    def set_clearing_price(self, commodity_id, lst):
        self.clearing_prices[commodity_id] = lst
        return lst

    def add_clearing_price(self, commodity_id, value):
        result = self.clearing_prices[commodity_id].append(value)
        lst = self.clearing_prices[commodity_id]
        if len(lst) > 15:
            lst.pop(0)
        return result

    def get_clearing_price_range(self, commodity_id):
        lst = self.get_clearing_price(commodity_id)
        return [min(lst), max(lst)]

    def get_clearing_favorability(self, value, min, max):
        value -= min
        max -= min
        min = 0
        value = value/(max-min)
        return value





    def generate_offers(self, bazaar, commodity_id):
        surplus = self.inventory.surplus(commodity_id)

        if surplus > 0:
            offer = self.create_ask(bazaar, commodity_id, 1)
            if offer:
                bazaar.ask(offer)
        else:
            shortage = self.inventory.shortage(commodity_id)
            space = self.inventory.get_space_empty()
            limit = 0
            if shortage > 0:
                limit = min([shortage, space])
                offer = self.create_bid(bazaar, commodity_id, limit)
                if offer:
                    bazaar.bid(offer)

    def create_bid(self, bazaar, commodity_id, limit):
        bid_price = self.determine_price(commodity_id)
        ideal = self.determine_buy_quantity(bazaar,commodity_id)

        quantity = min([ideal, limit])

        if quantity > 0:
            return Offer(self, commodity_id, quantity, bid_price)

    def create_ask(self, bazaar, commodity_id, limit):
        bid_price = self.determine_price(commodity_id)
        ideal = self.determine_sale_quantity(bazaar,commodity_id)

        quantity = min([ideal, limit])

        if quantity > 0:
            return Offer(self, commodity_id, quantity, bid_price)





    def get_inventory(self, commodity_id):
        return self.inventory.get_quantity(commodity_id)

    def change_inventory(self, commodity_id, delta):
        return self.inventory.change_quantity(commodity_id, delta)





    def get_money(self):
        return self.money

    def set_money(self, f):
        self.money = f
        return self.money

    def get_money_last(self):
        return self.money_last

    def set_money_last(self, f):
        self.money_last = f
        return self.money_last

    def get_profit(self):
        return self.profit




    def __repr__(self):
        str = "<Actor:%X Money: %r, Labor: %r, Inventory: %r>" % (id(self), self.money, self.labor_id, self.inventory.goods)
        return str