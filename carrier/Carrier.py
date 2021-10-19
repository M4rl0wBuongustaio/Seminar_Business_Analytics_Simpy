from order import BusinessOrder


class Carrier:
    def __init__(self, env, business_order):
        self.business_order = business_order
        self.env = env

    # Todo: implement different vehicle.
    def deliver_truck(self):
        business_add = self.business_order.get_business_add
        quantity = self.business_order.get_quantity
        material_type = self.business_order.get_material_type
        # One truck can carry 10 items.
        for i in range(quantity/10):
    # Todo: Implement delivery.