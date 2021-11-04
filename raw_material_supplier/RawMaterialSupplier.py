from carrier import Carrier


class RawMaterialSupplier:
    def __init__(self, env, business_order, material_type):
        self.env = env
        self.business_order = business_order
        self.material_type = material_type
        # self.initial_stock = initial_stock
        # Start the check_stock process everytime an instance is created.
        # self.action = env.process(self.check_stock(business_order, initial_stock))

    """
    def check_stock(self, business_order, initial_stock):
        while True:
            print('Order received. Checking stock at %d' % self.env.now)
            if business_order.get_quantity() > initial_stock.get_inventory():
                # Static order duration for raw_material_supplier is 5.
                print('The stock of raw materials must be replenished.')
                yield self.env.timeout(5)
                initial_stock.set_inventory(business_order.get_quantity - initial_stock.get_inventory())
                print('The stock of raw materials was replenished at %d' % self.env.now)
                return
            yield self.env.process(self.init_delivery(business_order))
    """

    def init_delivery(self, business_order):
        print('Delivery order has been sent to carrier at %d' % self.env.now)
        return Carrier.Carrier(business_order, self.env).calculate_delivery()
