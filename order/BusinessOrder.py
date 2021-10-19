class BusinessOrder:
    def __init__(self, quantity, material_type, business_add):
        self.quantity = quantity
        self.material_type = material_type
        # Address of the business customer.
        self.business_add = business_add

    def get_quantity(self):
        return self.quantity

    def get_material_type(self):
        return self.material_type

    def get_business_add(self):
        return self.business_add
