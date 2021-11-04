import simpy
import final_customer


env = simpy.Environment()
customer = final_customer.Customer(address=1, quantity=15)