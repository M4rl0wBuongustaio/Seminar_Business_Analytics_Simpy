

class Stock:
    def __init__(self, env, material_type, inventory, address, monitoring):
        self.env = env
        self.material_type = material_type
        self.inventory = inventory
        self.address = address
        self.monitoring = monitoring

    def get_material_type(self):
        return self.material_type

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        # material_type for Wholesaler = 0
        if self.material_type == 0:
            self.monitoring.append_data(date=self.env.now, inv_ws=inventory)
        # for material_type 1, 2 & 3 = Manufacturer
        elif self.material_type == 1:
            self.monitoring.append_data(date=self.env.now, inv_mr_1=inventory)
        elif self.material_type == 2:
            self.monitoring.append_data(date=self.env.now, inv_mr_2=inventory)
        elif self.material_type == 3:
            self.monitoring.append_data(date=self.env.now, inv_mr_3=inventory)
        self.inventory = inventory + self.get_inventory()

    def get_address(self):
        return self.address
