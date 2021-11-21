from random import seed, randint
import monitoring
import pandas as pd
import simpy
from customer import customer
from manufacturer import manufacturer
from stock import stock
from wholesaler import wholesaler

seed(25)

# Monitoring
initial_data = {'date': [0], 'inv_mr_1': [0], 'inv_mr_2': [0], 'inv_mr_3': [0], 'backorder_mr': [0], 'inv_ws': [0],
                'backorder_ws': [0], 'customer_name': [0], 'received_quantity': [0]}
data_frame = pd.DataFrame(initial_data, index=[1])
monitoring = monitoring.Monitoring(data_frame=data_frame, initial_data=initial_data)


def customer_generator(env, wholesaler):
    i = 1
    while env.now < 400:
        yield env.timeout(randint(2, 9))
        customer.Customer(env=env, address=randint(1, 5), name=i, wholesaler=wholesaler, quantity=randint(1, 35),
                          monitoring=monitoring)
        i = i + randint(1, 3)


env = simpy.Environment()
# Manufacturer
stock_1 = stock.Stock(env=env, material_type=1, inventory=0, safety_stock=0, address=3, monitoring=monitoring)
stock_2 = stock.Stock(env=env, material_type=2, inventory=0, safety_stock=0, address=3, monitoring=monitoring)
stock_3 = stock.Stock(env=env, material_type=3, inventory=0, safety_stock=0, address=3, monitoring=monitoring)
manufacturer = manufacturer.Manufacturer(env=env, address=3, stock_1=stock_1, stock_2=stock_2, stock_3=stock_3,
                                         monitoring=monitoring)
# Wholesaler
stock_ws = stock.Stock(env=env, material_type=0, inventory=0, safety_stock=0, address=2, monitoring=monitoring)
wholesaler = wholesaler.Wholesaler(env=env, stock=stock_ws, manufacturer=manufacturer, address=2, monitoring=monitoring)
# start of simulation
env.process(customer_generator(env=env, wholesaler=wholesaler))
# Go!
env.run(until=400)

# monitoring.print_sc_data()
# monitoring.save_sc_data()
