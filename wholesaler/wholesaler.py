import order.customer_order
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

    def check_stock(self, c_order: order.customer_order.CustomerOrder):
        order_quantity = c_order.get_quantity()
        if self.stock.get_inventory() >= order_quantity:
            if self.stock.get_reorder_point() > (self.stock.get_inventory() - order_quantity):
                self.initialize_business_order(quantity=self.stock.get_target_stock())
            transporter = carrier.Carrier(env=self.env, c_order=c_order)
            transporter.calculate_delivery()
            self.stock.decrease_inventory(quantity=order_quantity)
        else:
            self.initialize_business_order(quantity=self.stock.get_target_stock())
            self.add_backorder(c_order)

    def receive_customer_order(self, c_order):        self.check_stock(c_order)

    def receive_delivery(self, c_order):
        self.stock.increase_inventory(c_order.get_quantity())
        if self.backorder.qsize() > 1:
            self.check_stock(c_order=self.get_last_backorder())

    def initialize_business_order(self, quantity):
        c_order = customer_order.CustomerOrder(quantity=quantity, debtor=self)
        self.manufacturer.receive_customer_order(c_order)

    def get_last_backorder(self):
        backorder_ws = self.backorder.get()
        self.monitoring.append_data(date=self.env.now, backorder_ws=self.backorder.qsize())
        return backorder_ws

    def add_backorder(self, c_order):
        self.backorder.put(c_order)
        self.monitoring.append_data(date=self.env.now, backorder_ws=self.backorder.qsize())
