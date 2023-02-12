class SyntaxTree:
    def __init__(self):
        self.lookup = dict()
        self.list = []

    def add(self, item):
        key = item.name
        if key not in self.lookup:
            self.lookup[key] = item
            self.list.append(item)
