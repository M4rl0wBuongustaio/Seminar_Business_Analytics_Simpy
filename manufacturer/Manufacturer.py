import Monitoring as mT
import queue
from carrier import Carrier
from order import BusinessOrder
from raw_material_supplier import RawMaterialSupplier


class Manufacturer:
    def __init__(self, env, stock_1, stock_2, stock_3, address):
        self.env = env
        self.stock_1 = stock_1
        self.stock_2 = stock_2
        self.stock_3 = stock_3
        self.address = address
        self.backorder = queue.Queue()

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

    def receive_order(self, customer_order):
        self.env.process(self.add_backorder(customer_order))
        self.env.process(self.produce())

    def produce(self):
        customer_order = self.get_last_backorder()
        order_quantity = customer_order.get_quantity()
        # 1 Product = 20% resource_1; 30% resource_2; 50% resource_3
        required_material_1 = order_quantity() * 0.2
        required_material_2 = order_quantity() * 0.3
        required_material_3 = order_quantity() * 0.5
        if self.check_stock(required_material_1, required_material_2, required_material_3):
            self.stock_1.set_inventory(self.stock_1.get_inventory - required_material_1)
            self.stock_2.set_inventory(self.stock_2.get_inventory - required_material_2)
            self.stock_3.set_inventory(self.stock_3.get_inventory - required_material_3)
            # 1 time unit = 10 product units
            yield self.env.timeout(order_quantity / 10)
            self.env.process(self.initialize_delivery(customer_order))
        self.add_backorder(customer_order)

    # Without safety stock.
    def check_stock(self, rm1, rm2, rm3):
        if rm1 < self.stock_1.get_inventory():
            deviation_1 = rm1 - self.stock_1.get_inventory()
            self.env.process(self.initialize_order(deviation_1, self.stock_1.get_material_type()))
        elif rm2 < self.stock_2.get_inventory():
            deviation_2 = rm2 - self.stock_2.get_inventory()
            self.env.process(self.initialize_order(deviation_2, self.stock_2.get_material_type))
        elif rm3 < self.stock_3.get_inventory():
            deviation_3 = rm3 - self.stock_3.get_inventory()
            self.env.process(self.initialize_order(deviation_3, self.stock_3.get_material_type()))
        return True

    def initialize_order(self, deviation, material_type):
        business_order = BusinessOrder.BusinessOrder(quantity=deviation,
                                                     material_type=material_type,
                                                     customer=self)
        supplier = RawMaterialSupplier.RawMaterialSupplier(env=self.env,
                                                           business_order=business_order,
                                                           material_type=material_type)
        self.env.process(supplier.init_delivery())

    def initialize_delivery(self, order):
        carrier = Carrier.Carrier(self.env, order)
        self.env.process(carrier.calculate_delivery())

    def add_backorder(self, customer_order):
        backorder_mr = self.backorder.qsize() + 1
        mT.append_data(date=self.env.now, backorder_mr=backorder_mr)
        self.backorder.put(customer_order)

    def get_last_backorder(self):
        backorder_mr = self.backorder.qsize() - 1
        mT.append_data(date=self.env.now, backorder_mr=backorder_mr)
        return self.backorder.get()
