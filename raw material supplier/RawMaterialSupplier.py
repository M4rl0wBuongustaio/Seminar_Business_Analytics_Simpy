from carrier import Carrier


class RawMaterialSupplier:
    def __init__(self, env, business_order, stock):
        self.env = env
        self.business_order = business_order
        self.stock = stock
        # Start the check_stock process everytime an instance is created.
        self.action = env.process(self.check_stock(business_order, stock))

    def check_stock(self, business_order, stock):
        while True:
            print('Order received. Checking stock at %d' % self.env.now)
            if business_order.get_quantity() > stock.get_inventory():
                # Static order duration for raw material supplier is 5.
                print('The stock of raw materials must be replenished.')
                yield self.env.timeout(5)
                stock.set_inventory(business_order.get_quantity - stock.get_inventory())
                print('The stock of raw materials was replenished at %d' % self.env.now)
                return
            yield self.env.process(self.initialize_delivery(business_order))

    def initialize_delivery(self, business_order):
        print('Delivery order has been sent to carrier at %d' % self.env.now)
        return Carrier.Carrier(business_order, self.env).calculate_delivery()
