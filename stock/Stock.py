import Monitoring as mT


class Stock:
    def __init__(self, env, capacity, material_type, inventory, address):
        self.env = env
        self.capacity = capacity
        self.material_type = material_type
        self.inventory = inventory
        self.address = address

    def get_capacity(self):
        return self.capacity

    def get_material_type(self):
        return self.material_type

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        # material_type for Wholesaler = 0
        if self.material_type == 0:
            mT.append_data(date=self.env.now, inv_ws=inventory)
        # for material_type 1, 2 & 3 = Manufacturer
        elif self.material_type == 1:
            mT.append_data(date=self.env.now, inv_mr_1=inventory)
        elif self.material_type == 2:
            mT.append_data(date=self.env.now, inv_mr_2=inventory)
        elif self.material_type == 3:
            mT.append_data(date=self.env.now, inv_mr_3=inventory)
        self.inventory = inventory

    def get_address(self):
        return self.address
