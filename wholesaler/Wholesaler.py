from order.CustomerOrder import CustomerOrder
from carrier import Carrier
import queue


class Wholesaler:
    def __init__(self, env, stock, manufacturer, address):
        self.env = env
        self.stock = stock
        self.manufacturer = manufacturer
        self.address = address
        self.backorder = queue.Queue()

    def get_stock(self):
        return self.stock

    def get_manufacturer(self):
        return self.manufacturer

    def get_address(self):
        return self.address

    def check_stock(self):
        customer_order = self.get_backorder()
        if self.stock.get_inventory() < customer_order.get_quantity():
            # Without safety stock.
            self.env.process(self.initialize_order(self.stock.get_inventory() - customer_order.get_quantity()))
        carrier = Carrier.Carrier(self.env, customer_order)
        self.env.process(carrier.calculate_delivery())
        self.env.process(self.reduce_stock(customer_order.get_quantity()))

    def receive_customer_order(self, customer_order):
        self.env.process(self.add_backorder(customer_order))
        self.env.process(self.check_stock())

    def initialize_order(self, quantity):
        customer_order = CustomerOrder(self.env, quantity, self.address)
        self.manufacturer.receive_customer_order(customer_order)

    def get_backorder(self):
        return self.backorder.get()

    def add_backorder(self, customer_order):
        self.backorder.put(customer_order)

    def reduce_stock(self, quantity):
        current_stock = self.stock.get_inventory()
        self.env.process(self.stock.set_inventory(current_stock - quantity))


