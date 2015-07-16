__author__ = 'Petter'

class Inventory():

    def __init__(self):
        self.goods = {}
        self.ideal = {}
        self.size = 100



    #Goods Quantity Functions
    def set_quantity(self, commodity_id, quantity):
        self.goods[commodity_id] = quantity
        return self

    def get_quantity(self,commodity_id):
        return self.goods.get(commodity_id, 0)

    def change_quantity(self, commodity_id, delta_quantity):
        old_quantity = self.get_quantity(commodity_id)
        new_quantity = old_quantity+delta_quantity
        self.set_quantity(commodity_id, new_quantity)
        return self

    def contains(self, other):
        if not other:
            return True
        for k,v in other.items():
            if not self.get_quantity(k) >= v:
                return False
        return True



    #Ideal Quantity Functions
    def set_ideal_quantity(self, commodity_id, quantity):
        self.ideal[commodity_id] = quantity
        return self

    def get_ideal_quantity(self, commodity_id):
        return self.ideal.get(commodity_id, 0)

    def change_ideal_quantity(self, commodity_id, delta_quantity):
        old_quantity = self.get_ideal_quantity(commodity_id)
        new_quantity = old_quantity+delta_quantity
        self.set_ideal_quantity(commodity_id, new_quantity)
        return self



    # Inventory status Functions

    def surplus(self, commodity_id):
        ideal = self.get_ideal_quantity(commodity_id)
        actual = self.get_quantity(commodity_id)
        surplus = actual-ideal
        clamp = max([surplus, 0])
        return clamp

    def shortage(self, commodity_id):
        ideal = self.get_ideal_quantity(commodity_id)
        actual = self.get_quantity(commodity_id)
        shortage = ideal-actual
        clamp = max([shortage, 0])
        return clamp



    #Space Functions
    def get_space_empty(self):
        return self.size - self.get_space_used()

    def get_space_used(self):
        return sum([v for k,v in self.goods.items()])

