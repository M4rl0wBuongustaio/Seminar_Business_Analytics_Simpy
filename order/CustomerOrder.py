class CustomerOrder:
    def __init__(self, env, quantity, address, customer):
        self.env = env
        self.quantity = quantity
        self.address = address
        self.customer = customer

    def get_quantity(self):
        return self.quantity

    def get_address(self):
        return self.address

    def receive_order(self):
        print("Order received at %d" % self.env.now())

    def get_customer(self):
        return self.customer
