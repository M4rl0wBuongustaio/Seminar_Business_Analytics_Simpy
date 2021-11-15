from routing import ROUTING


class Carrier:
    def __init__(self, env, order):
        self.order = order
        self.env = env

    def calculate_delivery(self):
        for r_id, r in ROUTING.items():
            if r_id == self.order.get_address():
                for key in r.items():
                    if 'truck' in key[0]:
                        self.truck_delivery(delivery_step=key[0], delivery_duration=key[1])
                    elif 'ship' in key[0]:
                        self.delivery_ship(key[1])
                        continue
                raise Exception('Shipping method unknown!')
        raise Exception('Carrier could not identify delivery address!')

    def delivery_ship(self, delivery_duration):
        yield self.env.timeout(delivery_duration)
        return

    def truck_delivery(self, delivery_step, delivery_duration):
        if delivery_step == 'truck':
            yield self.env.timeout(delivery_duration)
            self.order.get_customer().receive_delivery(self.order)
            return
        elif delivery_step == 'truck1':
            yield self.env.timeout(delivery_duration)
        elif delivery_step == 'truck2':
            yield self.env.timeout(delivery_duration)
            self.order.get_customer().receive_delivery(self.order)
            return
