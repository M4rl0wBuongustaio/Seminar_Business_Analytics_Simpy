import Monitoring as mT
from order import CustomerOrder


class Customer:
    def __init__(self, env, address, quantity, name, wholesaler):
        self.env = env
        self.address = address
        self.quantity = quantity
        self.name = name
        self.wholesaler = wholesaler
        # Place order as soon as created.
        self.initialize_order()

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_quantity(self):
        return self.quantity

    def initialize_order(self):
        customer_order = CustomerOrder.CustomerOrder(quantity=self.quantity, customer=self)
        self.env.process(self.wholesaler.receive_customer_order(customer_order=customer_order))

    def receive_delivery(self, quantity):
        mT.append_data(received_quantity=quantity, customer_name=self.name)
        print('Customer ' + self.name + ' received a delivery of ' + quantity + ' items at ' + self.env.now())
