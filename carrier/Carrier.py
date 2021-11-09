from Routing import ROUTING


class Carrier:
    def __init__(self, env, order):
        self.order = order
        self.env = env

    def calculate_delivery(self):
        while True:
            for r_id, r in ROUTING:
                if r_id == self.order.get_address():
                    for key in r:
                        if 'truck' in key:
                            self.env.process(self.delivery_truck(delivery_duration=key.value(),
                                                                 delivery_step=key))
                            return
                        elif 'ship' in key:
                            self.env.process(self.delivery_ship(key.value()))
                            return
                    raise Exception('Shipping method unknown!')
            raise Exception('Carrier could not identify delivery address!')

    def delivery_truck(self, delivery_duration, delivery_step):
        if delivery_step == 'truck':
            yield self.env.timeout(delivery_duration)
            self.env.process(self.order.get_customer().receive_delivery(self.order.get_quantity()))
        elif delivery_step == 'truck1':
            yield self.env.timeout(delivery_duration)
        elif delivery_step == 'truck2':
            yield self.env.timeout(delivery_duration)
            self.env.process(self.order.get_customer().receive_delivery(self.order.get_quantity()))
        return

    def delivery_ship(self, delivery_duration):
        yield self.env.timeout(delivery_duration)
