class EnumDef:
    def __init__(self):
        self.name = ''
        self.items = []


class EnumItemDef:
    def __init__(self):
        self.key = 0
        self.name = ''
        self.display_name = ''


class StructDef:
    def __init__(self):
        self.name = ''
        self.items = []


class StructItemDef:
    def __init__(self):
        self.data_type = ''
        self.name = ''
        self.display_name = ''
        self.units = ''
        self.group = ''
        self.monitor = True
        self.dim = 0
