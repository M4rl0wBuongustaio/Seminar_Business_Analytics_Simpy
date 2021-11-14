from routing import ROUTING


class Carrier:
    def __init__(self, env, order):
        self.order = order
        self.env = env

    def calculate_delivery(self):
        while True:
            for r_id, r in ROUTING.items():
                if r_id == self.order.get_address():
                    for key in r.items():
                        if 'truck' in key:
                            self.delivery_truck(delivery_duration=key[1],
                                                delivery_step=key[0])
                            return
                        elif 'ship' in key:
                            self.delivery_ship(key[1])
                            return
                    raise Exception('Shipping method unknown!')
            raise Exception('Carrier could not identify delivery address!')

    def delivery_truck(self, delivery_duration, delivery_step):
        if delivery_step == 'truck':
            yield self.env.timeout(delivery_duration)
            self.order.get_customer().receive_delivery(self.order)
        elif delivery_step == 'truck1':
            yield self.env.timeout(delivery_duration)
        elif delivery_step == 'truck2':
            yield self.env.timeout(delivery_duration)
            self.order.get_customer().receive_delivery(self.order)
        return

    def delivery_ship(self, delivery_duration):
        yield self.env.timeout(delivery_duration)
