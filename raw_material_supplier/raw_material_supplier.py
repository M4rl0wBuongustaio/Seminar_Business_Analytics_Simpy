import order.raw_material_order
from carrier import carrier


class RawMaterialSupplier:
    def __init__(self, env, business_order, material_type):
        self.env = env
        self.business_order = business_order
        self.material_type = material_type
        self.duration = business_order.get_quantity()/2

    def init_delivery(self):
        # yield self.env.timeout(self.duration)
        transporter = carrier.Carrier(c_order=self.business_order, env=self.env)
        transporter.calculate_delivery()
