from order import Order
from raw_material_supplier import RawMaterialSupplier
from carrier import Carrier


def initialize_delivery(order, env):
    carrier = Carrier.Carrier(env, order)
    carrier.calculate_delivery()


class Manufacturer:
    def __init__(self, env, stock_1, stock_2, stock_3, customer_order, address):
        self.env = env
        self.stock_1 = stock_1
        self.stock_2 = stock_2
        self.stock_3 = stock_3
        self.customer_order = customer_order
        self.address = address

    def get_address(self):
        return self.address

    def receive_delivery(self, inventory, material_type):
        if self.stock_1.get_material_type() == material_type:
            self.stock_1.set_inventory(inventory + self.stock_1.get_inventory())
        elif self.stock_2.get_material_type() == material_type:
            self.stock_2.set_inventory(inventory + self.stock_2.get_inventory())
        elif self.stock_3.get_material_type() == material_type:
            self.stock_3.set_inventory(inventory + self.stock_3.get_inventory())
        return

    def produce(self):
        order_quantity = self.customer_order.get_quantity()
        required_material_1 = order_quantity() * 0.2
        required_material_2 = order_quantity() * 0.3
        required_material_3 = order_quantity() * 0.5
        if self.check_stock(required_material_1, required_material_2, required_material_3):
            self.stock_1.set_inventory(self.stock_1.get_inventory - required_material_1)
            self.stock_2.set_inventory(self.stock_2.get_inventory - required_material_2)
            self.stock_3.set_inventory(self.stock_3.get_inventory - required_material_3)
            # 1 time unit = 10 product units
            yield self.env.timeout(order_quantity / 10)
        initialize_delivery(self.customer_order, self.env)

    def check_stock(self, m1, m2, m3):
        if m1 < self.stock_1.get_inventory():
            deviation_1 = m1 - self.stock_1.get_inventory()
            self.initialize_order(deviation_1, self.stock_1.get_material_type())
        elif m2 < self.stock_2.get_inventory():
            deviation_2 = m2 - self.stock_2.get_inventory()
            self.initialize_order(deviation_2, self.stock_2.get_material_type)
        elif m3 < self.stock_3.get_inventory():
            deviation_3 = m3 - self.stock_3.get_inventory()
            self.initialize_order(deviation_3, self.stock_3.get_material_type())
        return True

    def initialize_order(self, deviation, material_type):
        order = Order.Order(quantity=deviation,
                            material_type=material_type,
                            customer=Manufacturer)
        rms = RawMaterialSupplier.RawMaterialSupplier(self.env, order, order.get_material_type())

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

    def __ne__(self, o: object) -> bool:
        return super().__ne__(o)
