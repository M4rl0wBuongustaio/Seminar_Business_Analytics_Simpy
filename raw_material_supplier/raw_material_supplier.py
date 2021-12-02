import order.raw_material_order
from carrier import carrier


class RawMaterialSupplier:
    def __init__(self, env, business_order: order.raw_material_order.RawMaterialOrder, material_type):
        self.env = env
        self.business_order = business_order
        self.material_type = material_type

    def init_delivery(self):
        transporter = carrier.Carrier(c_order=self.business_order, env=self.env)
        transporter.calculate_delivery()
