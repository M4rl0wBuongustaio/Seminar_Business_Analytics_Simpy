from routing import ROUTING


class Carrier:
    def __init__(self, env, c_order):
        self.c_order = c_order
        self.env = env

    def calculate_delivery(self):
        for r_id, r in ROUTING.items():
            if r_id == self.c_order.get_address():
                for key in r.items():
                    if 'truck' in key[0]:
                        self.env.process(self.truck_delivery(delivery_step=key[0], delivery_duration=key[1]))
                    elif 'ship' in key[0]:
                        self.env.process(self.ship_delivery(key[1]))
                        continue

    def ship_delivery(self, delivery_duration):
        yield self.env.timeout(delivery_duration)
        return

    def truck_delivery(self, delivery_step, delivery_duration):
        if delivery_step == 'truck':
            yield self.env.timeout(delivery_duration)
            self.c_order.get_customer().receive_delivery(self.c_order)
        elif delivery_step == 'truck1':
            yield self.env.timeout(delivery_duration)
        elif delivery_step == 'truck2':
            yield self.env.timeout(delivery_duration)
            self.c_order.get_customer().receive_delivery(self.c_order)
