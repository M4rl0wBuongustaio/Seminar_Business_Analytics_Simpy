import customer.customer
import order.customer_order
from routing import ROUTING_2


class Carrier:
    def __init__(self, env, c_order: order.customer_order.CustomerOrder):
        self.c_order = c_order
        self.env = env

    def calculate_delivery(self):
        for r_id, r in ROUTING_2.items():
            if r_id == self.c_order.get_address():
                for key in r.items():
                    if 'truck' in key[0]:
                        yield self.env.timeout(key[1])
                        self.c_order.get_customer().receive_delivery()
                        # self.truck_delivery(delivery_step=key[0], delivery_duration=key[1])
                    elif 'ship' in key[0]:
                        self.ship_delivery(key[1])
                        continue
                raise Exception('Shipping method unknown!')
        raise Exception('Carrier could not identify delivery address!')

    def ship_delivery(self, delivery_duration):
        yield self.env.timeout(delivery_duration)
        return

    def truck_delivery(self, delivery_step, delivery_duration):
        if delivery_step == 'truck':
            yield self.env.timeout(delivery_duration)
            self.c_order.get_customer().receive_delivery(self.c_order)
            return
        elif delivery_step == 'truck1':
            yield self.env.timeout(delivery_duration)
        elif delivery_step == 'truck2':
            yield self.env.timeout(delivery_duration)
            self.c_order.get_customer().receive_delivery(self.c_order)
            return
