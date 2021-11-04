
class Customer:
    def __init__(self, address, quantity):
        self.address = address
        self.quantity = quantity

    def get_address(self):
        return self.address

    def get_quantity(self):
        return self.quantity
