import order.customer_order
from order import customer_order


class Customer:
    def __init__(self, env, address, quantity, name, wholesaler, monitoring):
        self.env = env
        self.address = address
        self.quantity = quantity
        self.name = name
        self.wholesaler = wholesaler
        self.monitoring = monitoring
        self.initialize_order()

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_quantity(self):
        return self.quantity

    def initialize_order(self):
        c_order = customer_order.CustomerOrder(quantity=self.quantity, debtor=self)
        self.wholesaler.receive_customer_order(c_order=c_order)

    def receive_delivery(self, c_order: order.customer_order.CustomerOrder):
        quantity = c_order.get_quantity()
        name = self.name
        self.monitoring.append_data(date=self.env.now, received_quantity=quantity,
                                    customer_name=name)
        print('Customer: ' + str(name) + ' received and delivery of:' + str(quantity))
