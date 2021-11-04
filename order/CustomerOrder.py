class CustomerOrder:
    def __init__(self, env, quantity, address):
        self.env = env
        self.quantity = quantity
        self.address = address

    def get_quantity(self):
        return self.quantity

    def get_address(self):
        return self.address

    def receive_order(self):
        print("Order received ad %d" % self.env.now())
