import enum
import struct


class BsonGenerator:
    def __init__(self):
        self.raw_data = bytearray()
        self.element_count = 0
        self.stack = []
        self.depth = 0

    def stack_push(self):

    def start_unnamed_object(self):

        pass

    def start_object(self, key=None):
        pass

    def end_object(self):
        pass

    def start_array(self, key):
        pass

    def end_array(self):
        pass

    def add_string(self, value, key=None):
        pass

    def add_boolean(self, value, key=None):
        if key is None:
            key = str(self.element_count)

        self.__append_uint8(BsonConstants.bson_bool)
        self.__append_cstring(key)
        self.__append_uint8(BsonConstants.bson_bool_true if value else BsonConstants.bson_bool_false)
        self.element_count += 1

    def add_int32(self, value, key=None):
        if key is None:
            key = str(self.element_count)

        self.element_count += 1
        self.__append_uint8(BsonConstants.bson_int32)
        self.__append_cstring(key)
        self.__append_int32(value)

    def add_double(self, value, key=None):

        pass

    def __append_byte(self, value):
        self.raw_data.append(value)

    def __append_uint8(self, value):
        self.raw_data.append(value)

    def __append_cstring(self, value):
        value = str(value)
        if value:
            for c in value:
                self.raw_data.append(ord(c))
        self.__append_byte(0)

    def __append_int32(self, value):
        self.raw_data.extend(struct.pack("<i", value))

    def __append_uint64(self, value):
        self.raw_data.extend(struct.pack("<Q", value))

    def __append_int64(self, value):
        self.raw_data.extend(struct.pack("<q", value))

    def __append_double(self, value):
        self.raw_data.extend(struct.pack("<d", value))


class BsonConstants(enum.Enum):
    bson_end_of_object = 0
    bson_double = 1
    bson_string = 2
    bson_document = 3
    bson_array = 4
    bson_bool_false = 0
    bson_bool_true = 1
    bson_bool = 8
    bson_int32 = 16

