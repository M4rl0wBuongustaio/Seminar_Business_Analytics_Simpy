from manufacturer import Manufacturer


class BusinessOrder:
    def __init__(self, quantity, material_type, customer):
        self.quantity = quantity
        self.material_type = material_type
        # Customer = Manufacturer or Final Customer
        self.customer = customer

    def get_quantity(self):
        return self.quantity

    # Only relevant for business_orders.
    def get_material_type(self):
        return self.material_type

    def get_address(self):
        return self.customer.get_address()

    def get_customer(self):
        return self.customer
