import simpy
import itertools
from random import seed, randint
from Customer import Customer
from manufacturer import Manufacturer
from stock import Stock
from wholesaler import Wholesaler
import Monitoring as mT

seed(25)


def customer_generator(env, wholesaler):
    for i in itertools.count():
        yield env.timeout(randint(5, 35))
        Customer.Customer(env=env, address=randint(1, 5), name=i, wholesaler=wholesaler,
                          quantity=randint(1, 15))


env = simpy.Environment()
stock_1 = Stock.Stock(env=env, material_type=1, inventory=0, address=3)
stock_2 = Stock.Stock(env=env, material_type=2, inventory=0, address=3)
stock_3 = Stock.Stock(env=env, material_type=3, inventory=0, address=3)
manufacturer = Manufacturer.Manufacturer(env=env, address=3, stock_1=stock_1, stock_2=stock_2, stock_3=stock_3)
stock_ws = Stock.Stock(env=env, material_type=0, inventory=0, address=2)
wholesaler = Wholesaler.Wholesaler(env=env, stock=stock_ws, manufacturer=manufacturer, address=2)
env.process(customer_generator(env=env, wholesaler=wholesaler))

env.run(until=400)

print(mT.sc_data)
