import queue

import order.customer_order
from carrier import carrier
from order import raw_material_order, customer_order
from raw_material_supplier import raw_material_supplier


class Manufacturer:
    def __init__(self, env, stock_1, stock_2, stock_3, address, monitoring):
        self.env = env
        self.stock_1 = stock_1
        self.stock_2 = stock_2
        self.stock_3 = stock_3
        self.address = address
        self.monitoring = monitoring
        self.backorder = queue.Queue()
        self.job_list = {}

    def get_address(self):
        return self.address

    def receive_delivery(self, rm_order: raw_material_order.RawMaterialOrder):
        target_customer_id = rm_order.get_target_customer_id()
        quantity = rm_order.get_quantity()
        material_type = rm_order.get_material_type()
        if self.stock_1.get_material_type() == material_type:
            self.stock_1.set_inventory(quantity)
        elif self.stock_2.get_material_type() == material_type:
            self.stock_2.set_inventory(quantity)
        elif self.stock_3.get_material_type() == material_type:
            self.stock_3.set_inventory(quantity)
        self.job_list[target_customer_id][material_type] = 0
        if all(value == 0 for value in self.job_list.values()):
            self.produce(c_order=self.get_last_backorder())

    def receive_customer_order(self, c_order):
        self.produce(c_order)

    def produce(self, c_order: customer_order.CustomerOrder):
        order_quantity = c_order.get_quantity()
        # 1 Product = 20% resource_1; 30% resource_2; 50% resource_3
        required_material_1 = order_quantity * 0.2
        required_material_2 = order_quantity * 0.3
        required_material_3 = order_quantity * 0.5
        if self.check_stock(customer_id=c_order.get_ident(), rm1=required_material_3,
                            rm2=required_material_2, rm3=required_material_3):
            self.stock_1.set_inventory(self.stock_1.get_inventory() - required_material_1)
            self.stock_2.set_inventory(self.stock_2.get_inventory() - required_material_2)
            self.stock_3.set_inventory(self.stock_3.get_inventory() - required_material_3)
            self.initialize_delivery(c_order)
        self.add_backorder(c_order)

    def check_stock(self, customer_id, rm1, rm2, rm3):
        rm1_ordered = rm2_ordered = rm3_ordered = enough_stock = False
        while not enough_stock:
            if rm1 > self.stock_1.get_inventory() and not rm1_ordered:
                self.initialize_business_order(quantity=rm1, material_type=self.stock_1.get_material_type(),
                                               target_customer_id=customer_id)
                rm1_ordered = True
                continue
            elif rm2 > self.stock_2.get_inventory() and not rm2_ordered:
                self.initialize_business_order(quantity=rm2, material_type=self.stock_2.get_material_type,
                                               target_customer_id=customer_id)
                rm2_ordered = True
                continue
            elif rm3 > self.stock_3.get_inventory() and not rm3_ordered:
                self.initialize_business_order(quantity=rm3, material_type=self.stock_3.get_material_type(),
                                               target_customer_id=customer_id)
                rm3_ordered = True
                continue
            elif rm1_ordered or rm2_ordered or rm3_ordered:
                return False
            return True

    def initialize_business_order(self, quantity, material_type, target_customer_id):
        self.job_list[target_customer_id] = {}
        self.job_list[target_customer_id][material_type] = quantity
        b_order = raw_material_order.RawMaterialOrder(quantity=quantity, material_type=material_type, customer=self,
                                                      target_customer_id=target_customer_id)
        supplier = raw_material_supplier.RawMaterialSupplier(env=self.env,
                                                             business_order=b_order,
                                                             material_type=material_type)
        supplier.init_delivery()

    def initialize_delivery(self, c_order: customer_order.CustomerOrder):
        transporter = carrier.Carrier(self.env, c_order)
        transporter.calculate_delivery()

    def add_backorder(self, backorder: order.customer_order.CustomerOrder):
        backorder_mr = self.backorder.qsize() + 1
        self.monitoring.append_data(date=self.env.now, backorder_mr=backorder_mr)
        self.backorder.put(backorder)

    def get_last_backorder(self):
        backorder_mr = self.backorder.qsize() - 1
        self.monitoring.append_data(date=self.env.now, backorder_mr=backorder_mr)
        return self.backorder.get()
