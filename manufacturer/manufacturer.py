import queue

import order.customer_order
import stock.stock
from carrier import carrier
from order import raw_material_order, customer_order
from raw_material_supplier import raw_material_supplier


class Manufacturer:
    def __init__(self, env, stock_1, stock_2, stock_3, address, monitoring):
        self.env = env
        self.stock_1: stock.stock.Stock = stock_1
        self.stock_2: stock.stock.Stock = stock_2
        self.stock_3: stock.stock.Stock = stock_3
        self.address = address
        self.monitoring = monitoring
        self.backorder = queue.Queue()
        self.job_list = {}

    def get_address(self):
        return self.address

    def receive_delivery(self, rm_order):
        quantity = rm_order.get_quantity()
        material_type = rm_order.get_material_type()
        if self.stock_1.get_material_type() == material_type:
            self.stock_1.increase_inventory(quantity)
        elif self.stock_2.get_material_type() == material_type:
            self.stock_2.increase_inventory(quantity)
        elif self.stock_3.get_material_type() == material_type:
            self.stock_3.increase_inventory(quantity)
        if self.backorder.qsize() > 1:
            self.produce(c_order=self.get_last_backorder())

    def receive_customer_order(self, c_order: order.customer_order.CustomerOrder):
        self.produce(c_order)

    def produce(self, c_order: customer_order.CustomerOrder):
        order_quantity = c_order.get_quantity()
        # 1 Product = 20% resource_1; 30% resource_2; 50% resource_3
        required_material_1 = order_quantity * 0.2
        required_material_2 = order_quantity * 0.3
        required_material_3 = order_quantity * 0.5
        if self.check_stock(rm1=required_material_1, rm2=required_material_2, rm3=required_material_3):
            self.stock_1.decrease_inventory(required_material_1)
            self.stock_2.decrease_inventory(required_material_2)
            self.stock_3.decrease_inventory(required_material_3)
            self.initialize_delivery(c_order)
        else:
            self.add_backorder(c_order)

    def check_stock(self, rm1, rm2, rm3):
        out_of_rm1 = out_of_rm2 = out_of_rm3 = True
        while True:
            if self.stock_1.get_inventory() >= rm1 and out_of_rm1:
                out_of_rm1 = False
                if self.stock_1.get_reorder_point() > (self.stock_1.get_inventory() - rm1):
                    self.initialize_business_order(
                        quantity=self.stock_1.get_target_stock(),
                        material_type=self.stock_1.get_material_type())
                continue
            elif self.stock_2.get_inventory() >= rm2 and out_of_rm2:
                out_of_rm2 = False
                if self.stock_2.get_reorder_point() > (self.stock_2.get_inventory() - rm2):
                    self.initialize_business_order(
                        quantity=self.stock_2.get_target_stock(),
                        material_type=self.stock_2.get_material_type())
                continue
            elif self.stock_3.get_inventory() >= rm3 and out_of_rm3:
                out_of_rm3 = False
                if self.stock_3.get_reorder_point() > (self.stock_3.get_inventory() - rm3):
                    self.initialize_business_order(
                        quantity=self.stock_3.get_target_stock(),
                        material_type=self.stock_3.get_material_type())
                continue
            elif out_of_rm1 or out_of_rm2 or out_of_rm3:
                if out_of_rm1:
                    self.initialize_business_order(quantity=self.stock_1.get_target_stock(),
                                                   material_type=self.stock_1.get_material_type())
                elif out_of_rm2:
                    self.initialize_business_order(quantity=self.stock_2.get_target_stock(),
                                                   material_type=self.stock_2.get_material_type())
                elif out_of_rm3:
                    self.initialize_business_order(quantity=self.stock_3.get_target_stock(),
                                                   material_type=self.stock_3.get_material_type())
                return False
            return True

    def initialize_business_order(self, quantity, material_type):
        b_order = raw_material_order.RawMaterialOrder(quantity=quantity, material_type=material_type, customer=self)
        supplier = raw_material_supplier.RawMaterialSupplier(env=self.env,
                                                             business_order=b_order,
                                                             material_type=material_type)
        supplier.init_delivery()

    def initialize_delivery(self, c_order: customer_order.CustomerOrder):
        transporter = carrier.Carrier(self.env, c_order)
        transporter.calculate_delivery()

    def add_backorder(self, backorder: order.customer_order.CustomerOrder):
        self.backorder.put(backorder)
        self.monitoring.append_data(date=self.env.now, backorder_mr=self.backorder.qsize())

    def get_last_backorder(self):
        backorder = self.backorder.get()
        self.monitoring.append_data(date=self.env.now, backorder_mr=self.backorder.qsize())
        return backorder
