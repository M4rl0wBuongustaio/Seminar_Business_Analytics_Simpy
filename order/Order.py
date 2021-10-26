# Stock that contains

class Order:
    def __init__(self, quantity, material_type, address):
        self.quantity = quantity
        self.material_type = material_type
        # Address of the (business) customer.
        self.address = address

    def get_quantity(self):
        return self.quantity

    # Only relevant for business_orders.
    def get_material_type(self):
        return self.material_type

    def get_address(self):
        return self.address

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

    def __ne__(self, o: object) -> bool:
        return super().__ne__(o)
