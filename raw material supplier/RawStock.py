class RawStock:
    def __init__(self, capacity, material_type, inventory):
        self.capacity = capacity
        self.material_type = material_type
        self. inventory = inventory

    def get_capacity(self):
        return self.capacity

    def get_material_type(self):
        return self.material_type

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        self.inventory = inventory

