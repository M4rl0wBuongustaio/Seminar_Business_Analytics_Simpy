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

# simulation environment
run_time = 400


def customer_generator(env, wholesaler):
    i = 1
    while env.now < run_time:
        yield env.timeout(2)
        customer.Customer(env=env, address=randint(1, 5), name=i, wholesaler=wholesaler, quantity=20,
                          monitoring=monitoring)
        i += 1


env = simpy.Environment()
# Manufacturer
address = 2
stock_1 = stock.Stock(env=env, material_type=1, inventory=2000, safety_stock=2000, address=address, monitoring=monitoring)
stock_2 = stock.Stock(env=env, material_type=2, inventory=2000, safety_stock=2000, address=address, monitoring=monitoring)
stock_3 = stock.Stock(env=env, material_type=3, inventory=2000, safety_stock=2000, address=address, monitoring=monitoring)
manufacturer = manufacturer.Manufacturer(env=env, address=address, stock_1=stock_1, stock_2=stock_2, stock_3=stock_3,
                                         monitoring=monitoring)
# Wholesaler
stock_ws = stock.Stock(env=env, material_type=0, inventory=0, safety_stock=0, address=2, monitoring=monitoring)
wholesaler = wholesaler.Wholesaler(env=env, stock=stock_ws, manufacturer=manufacturer, address=2, monitoring=monitoring)
# start of simulation
env.process(customer_generator(env=env, wholesaler=wholesaler))
# go!
env.run(until=run_time)

# monitoring.print_sc_data()
# monitoring.save_sc_data()

print(monitoring.get_sc_data().to_string())
