import customer.customer


class CustomerOrder:
    def __init__(self, quantity, debtor, ident):
        self.quantity = quantity
        self.debtor = debtor
        self.ident = ident

    def get_quantity(self):
        return self.quantity

    def get_customer(self):
        return self.debtor

    def get_address(self):
        return self.debtor.get_address()

    def get_ident(self):
        return self.ident
