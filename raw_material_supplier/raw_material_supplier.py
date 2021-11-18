from carrier import carrier


class RawMaterialSupplier:
    def __init__(self, env, business_order, material_type):
        self.env = env
        self.business_order = business_order
        self.material_type = material_type

    def init_delivery(self):
        transporter = carrier.Carrier(c_order=self.business_order, env=self.env)
        print('Delivery order has been sent to carrier at %d' % self.env.now)
        transporter.calculate_delivery()