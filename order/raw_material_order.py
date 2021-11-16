class RawMaterialOrder:
    def __init__(self, quantity, material_type, customer, target_customer_id):
        self.quantity = quantity
        self.material_type = material_type
        self.customer = customer
        # id for identifying the Wholesaler, because of whom the raw material order has been placed.
        self.target_customer_id = target_customer_id

    def get_quantity(self):
        return self.quantity

    # Only relevant for business_orders.
    def get_material_type(self):
        return self.material_type

    def get_address(self):
        return self.customer.get_address()

    def get_customer(self):
        return self.customer

    def get_target_customer_id(self):
        return self.target_customer_id
