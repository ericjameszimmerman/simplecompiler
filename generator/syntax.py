class EnumDef:
    def __init__(self):
        self.name = ''
        self.lookup = dict()
        self.items = []
        self.next_value = 0

    def add(self, enum_item):
        if enum_item:
            if enum_item.key is not None:
                target_key = enum_item.key
            else:
                target_key = self.next_value

            if enum_item.name not in self.lookup:
                enum_item.key = target_key
                self.lookup[enum_item.name] = enum_item
                self.items.append(enum_item)
                self.next_value = target_key + 1
            else:
                raise Exception('syntax error: duplicate enum')


class EnumItemDef:
    def __init__(self):
        self.key = None
        self.name = ''
        self.display_name = ''


class StructDef:
    def __init__(self):
        self.name = ''
        self.lookup = dict()
        self.items = []

    def add(self, struct_item):
        if struct_item:
            if struct_item.name not in self.lookup:
                self.lookup[struct_item.name] = struct_item
                self.items.append(struct_item)
            else:
                raise Exception('syntax error: duplicate struct')


class StructItemDef:
    def __init__(self):
        self.data_type = ''
        self.name = ''
        self.display_name = ''
        self.units = ''
        self.group = ''
        self.monitor = True
        self.dim = 0


class PropertyList:
    def __init__(self):
        self.lookup = dict()
        self.items = []

    def add_property(self, key, value, typeid):
        if key not in self.lookup:
            new_property = Property(key, value, typeid=typeid)
            self.lookup[key] = new_property
            self.items.append(new_property)

class Property:
    def __init__(self, key, value, typeid = None):
        self.key = key
        self.value = value
        self.typeid = typeid
