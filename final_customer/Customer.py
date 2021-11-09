class Customer:
    def __init__(self, env, address, quantity):
        self.env = env
        self.address = address
        self.quantity = quantity

    def get_address(self):
        return self.address

    def get_quantity(self):
        return self.quantity

    def receive_delivery(self, quantity):
        print('Customer received a delivery of ' + quantity + ' items at ' + self.env.now())
