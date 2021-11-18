import customer.customer


class CustomerOrder:
    def __init__(self, quantity, debtor):
        self.quantity = quantity
        self.debtor = debtor

    def get_quantity(self):
        return self.quantity

    def get_customer(self):
        return self.debtor

    def get_address(self):
        return self.debtor.get_address()

    def get_ident(self):
        return id(self)
