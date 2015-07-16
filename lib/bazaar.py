__author__ = 'Petter'
from collections import defaultdict
from random import shuffle, choice


class Bazaar():
    def __init__(self,commodities, actors):
        self.history = defaultdict(lambda: defaultdict(list))
        self.actors = actors
        self.offers = defaultdict(lambda: defaultdict(list))
        self.commodities = commodities
        self.labors = None

        self.init()

        for actor in actors:
            actor.init(self)



    def init(self):
        for commodity, recipe in self.commodities.items():
            price = sum(recipe.values())+1
            self.add_history("price", commodity, price * 0.5)
            self.add_history("price", commodity, price * 1.5)

    def simulate(self, rounds):
        for r in range(0,rounds):
            for actor in self.actors:
                actor.set_money_last(actor.money)
                #Here actor must performe production and consumption
                actor.produce(self)
                for commodity_id in self.commodities.keys():
                    actor.generate_offers(self, commodity_id)

            for commodity_id in self.commodities.keys():
                self.resolve_offers(commodity_id)

            for actor in self.actors:
                if actor.get_money() <= 0:
                    self.replace_actor(actor)


    #Offer Functions
    def ask(self, offer):
        if offer:
            self.offers[offer.commodity_id]["ask"].append(offer)
        return True

    def bid(self, offer):
        if offer:
            self.offers[offer.commodity_id]["bid"].append(offer)
        return True

    def resolve_offers(self, commodity_id):
        bids = self.offers[commodity_id]["bid"]
        shuffle(bids)
        bids.sort(key=lambda x: x.price, reverse = True)

        asks = self.offers[commodity_id]["ask"]
        shuffle(asks)
        asks.sort(key=lambda x: x.price)

        successful_trades = 0
        money_traded = 0
        units_traded = 0
        avg_price = 0
        num_asks = sum([o.quantity for o in asks])
        num_bids = sum([o.quantity for o in bids])

        while asks and bids:
            buyer = bids[0]
            seller = asks[0]
            quantity_traded = min([seller.quantity, buyer.quantity])
            clearing_price = (seller.price+buyer.price)/2

            if quantity_traded > 0:
                seller.quantity -= quantity_traded
                buyer.quantity -= quantity_traded

                self.transfer_commodity(commodity_id, quantity_traded, seller, buyer)
                self.transfer_money(quantity_traded*clearing_price, seller, buyer)

                buyer.actor.update_belief(self, "buy", commodity_id, True, clearing_price)
                buyer.actor.update_belief(self, "sell", commodity_id, True, clearing_price)

                money_traded += quantity_traded*clearing_price
                units_traded += quantity_traded
                successful_trades += 1

            if seller.quantity == 0:
                asks.pop(0)
            if buyer.quantity == 0:
                bids.pop(0)

        while bids:
            offer = bids.pop(0)
            offer.actor.update_belief(self, "buy", commodity_id, False)

        while asks:
            offer = asks.pop(0)
            offer.actor.update_belief(self, "sell", commodity_id, False)

        self.add_history("asks", commodity_id, num_asks)
        self.add_history("bids", commodity_id, num_bids)
        self.add_history("trades", commodity_id, units_traded)

        if units_traded > 0:
            avg_price = money_traded*1.0/units_traded
            self.add_history("price", commodity_id, avg_price)
        else:
            self.add_history("price", commodity_id, self.get_history("price", commodity_id, 1))

        return True


    def transfer_commodity(self, commodity_id, quantity, seller, buyer):
        seller.actor.change_inventory(commodity_id, -quantity)
        buyer.actor.change_inventory(commodity_id, +quantity)
        return True

    def transfer_money(self, quantity, seller, buyer):
        seller.actor.money += quantity
        buyer.actor.money -= quantity
        return True




    #History Functions
    def avg_history(self, type, commodity_id, lookback):
        lst = self.history[type][commodity_id]
        lookback = min([len(lst), lookback])
        return sum([v for v in lst[-lookback:]])/lookback

    def add_history(self, type, commodity_id, value):
        self.history[type][commodity_id].append(value)
        lst = self.history[type][commodity_id]
        if len(lst) > 15:
            lst.pop(0)
        return lst

    def set_history(self, type, commodity_id, lst):
        self.history[type][commodity_id] = lst
        return lst

    def get_history(self,type, commodity_id, i=None):
        if i:
            return self.history[type][commodity_id][i]
        else:
            return self.history[type][commodity_id]



    #Respawn functions
    def replace_actor(self, actor):
        pass

    def get_inventory_avg(self, labor_id, commodity_id):
        pass

    def get_labor_that_makes_most_of(self, commodity_id):
        pass

    def get_labor_with_most_of(self, commodity_id):
        pass

    def get_best_market_opportunity(self, minimum, lookback):
        pass

    def get_most_profitable_labor(self, lookback):
        return choice(list(self.commodities.keys()))


    def get_labor(self, labor_id):
        pass




    #Count Functions

    def commodity_count(self):
        return len(self.commodities)

    def actor_count(self):
        return len(self.actors)