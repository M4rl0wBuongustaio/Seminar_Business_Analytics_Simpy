class Stock:
    def __init__(self, env, material_type, inventory, safety_stock, address, monitoring):
        self.env = env
        self.material_type = material_type
        self.inventory = inventory
        self.safety_stock = safety_stock
        self.address = address
        self.monitoring = monitoring
        self.increase_inventory(0)

    def get_material_type(self):
        return self.material_type

    def get_inventory(self):
        return self.inventory

    def get_safety_stock(self):
        return self.safety_stock

    def increase_inventory(self, quantity):
        self.inventory = quantity + self.get_inventory()
        self.monitor_inventory()

    def decrease_inventory(self, quantity):
        self.inventory = self.get_inventory() - quantity
        self.monitor_inventory()

    def get_address(self):
        return self.address

    def monitor_inventory(self):
        current_inventory = self.get_inventory()
        if self.material_type == 0:
            self.monitoring.append_data(date=self.env.now, inv_ws=current_inventory)
        # for material_type 1, 2 & 3 = Manufacturer
        elif self.material_type == 1:
            self.monitoring.append_data(date=self.env.now, inv_mr_1=current_inventory)
        elif self.material_type == 2:
            self.monitoring.append_data(date=self.env.now, inv_mr_2=current_inventory)
        elif self.material_type == 3:
            self.monitoring.append_data(date=self.env.now, inv_mr_3=current_inventory)
