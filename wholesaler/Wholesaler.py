from order.CustomerOrder import CustomerOrder


class Wholesaler:
    def __init__(self, env, stock, manufacturer, address):
        self.env = env
        self.stock = stock
        self.manufacturer = manufacturer
        self.address = address

    def get_stock(self):
        return self.stock

    def get_manufacturer(self):
        return self.manufacturer

    def get_address(self):
        return self.address

    def check_stock(self, customer_order):
        if self.stock.get_inventory() < customer_order.get_quantity():
            self.initialize_order(self.stock.get_inventory() - customer_order.get_quantity())
        return True

    def receive_order(self, customer_order):
        # TODO: env needed?
        self.check_stock(customer_order)

    def initialize_order(self, quantity):
        customer_order = CustomerOrder(self.env, quantity, self.address)
        self.manufacturer.receive_order(customer_order)
