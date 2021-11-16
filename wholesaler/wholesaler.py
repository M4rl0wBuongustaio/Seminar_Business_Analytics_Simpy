import random

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

    def check_stock(self, order):
        order_quantity = order.get_quantity()
        if self.stock.get_inventory() < order_quantity:
            # Without safety stock.
            self.add_backorder(order)
            self.initialize_business_order(quantity=order_quantity, c_order_id=id(order))
            return
        transporter = carrier.Carrier(env=self.env, c_order=order)
        transporter.calculate_delivery()
        self.reduce_stock(order_quantity)
        return

    def receive_customer_order(self, order):
        self.check_stock(order)

    def receive_delivery(self, order):
        self.stock.set_inventory(order.get_quantity())
        self.check_stock(order=self.get_last_backorder())

    def initialize_business_order(self, quantity, c_order_id):
        order = customer_order.CustomerOrder(quantity=quantity, debtor=self, ident=c_order_id)
        self.manufacturer.receive_customer_order(order)

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
