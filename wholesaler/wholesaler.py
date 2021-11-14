from order import customer_order
from carrier import carrier
import queue


class Wholesaler:
    def __init__(self, env, stock, manufacturer, address, monitoring):
        self.env = env
        self.stock = stock
        self.manufacturer = manufacturer
        self.address = address
        self.backorder = queue.Queue()
        self.monitoring = monitoring

    def get_stock(self):
        return self.stock

    def get_manufacturer(self):
        return self.manufacturer

    def get_address(self):
        return self.address

    def check_stock(self):
        order = self.get_last_backorder()
        if self.stock.get_inventory() < order.get_quantity():
            # Without safety stock.
            self.initialize_business_order(self.stock.get_inventory() - order.get_quantity())
        transporter = carrier.Carrier(self.env, order)
        transporter.calculate_delivery()
        self.reduce_stock(order.get_quantity())

    def receive_customer_order(self, order):
        self.add_backorder(order)
        self.check_stock()

    def initialize_business_order(self, quantity):
        order = customer_order.CustomerOrder(quantity=quantity, customer=self)
        self.manufacturer.receive_order(order)

    def get_last_backorder(self):
        backorder_ws = self.backorder.qsize() - 1
        self.monitoring.append_data(date=self.env.now, backorder_ws=backorder_ws)
        return self.backorder.get()

    def add_backorder(self, order):
        backorder_ws = self.backorder.qsize() + 1
        self.monitoring.append_data(date=self.env.now, backorder_ws=backorder_ws)
        self.backorder.put(order)

    def reduce_stock(self, quantity):
        current_stock = self.stock.get_inventory()
        self.stock.set_inventory(current_stock - quantity)
