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
        oder = customer_order.CustomerOrder(quantity=self.quantity, customer=self)
        self.wholesaler.receive_customer_order(order=oder)

    def receive_delivery(self, order: customer_order.CustomerOrder):
        self.monitoring.append_data(date=self.env.now, received_quantity=order.get_quantity(), customer_name=self.name)
        print('customer ' + self.name + ' received a delivery of ' + order.get_quantity() + ' items at ' + self.env.now)
