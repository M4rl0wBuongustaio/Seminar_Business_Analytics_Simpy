class CustomerOrder:
    def __init__(self, quantity, customer):
        self.quantity = quantity
        self.customer = customer

    def get_quantity(self):
        return self.quantity

    def get_customer(self):
        return self.customer

    def get_address(self):
        return self.customer.get_address()
