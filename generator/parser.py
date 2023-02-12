import re
from .lexer import Lexer
from .lexer import TokenType
from .syntax import *

class Parser:
    def __init__(self, lexer, ast_data):
        self.lexer = lexer
        self.ast_data = ast_data
        self.token = None
        self.keywords = [
            'enum',
            'struct'
        ]

        self.subparsers = {
            'enum': self.parse_enum,
            'struct': self.parse_struct,
        }

        self.hex_regex = re.compile('^0[xX][0-9a-fA-F]+$')
        self.binary_regex = re.compile('^0[bB][0-1]+$')
        self.number_regex = re.compile('^\\d+\\.?\\d*$')
        self.integer_regex = re.compile('^\\d*$')

    def parse(self):
        self.lexer.keywords = self.keywords

        while True:
            token = self.lexer.get_token()
            if token:
                if token.kind == TokenType.KEYWORD:
                    if token.text in self.subparsers:
                        item = self.subparsers[token.text]()
                        if item:
                            self.ast_data.add(item)
                else:
                    raise Exception('syntax error')
            else:
                break

    def next_token(self):
        self.token = self.lexer.get_token()

    def peek_next_token(self):
        return self.lexer.peek_token()

    def parse_name_token(self):
        self.next_token()
        if self.token.kind == TokenType.VALUE:
            # future: add rules for name validation?
            return self.token.text
        else:
            raise Exception('unexpected token type')

    def parse_integer(self, value):
        if value is not None and len(value) > 0:
            if self.integer_regex.match(value):
                result = int(value)
            elif self.hex_regex.match(value):
                result = int(value, 16)
            else:
                raise Exception('syntax error: invalid integer')
        else:
            raise Exception('syntax error: invalid integer (null)')

        return result

    def parse_integer_token(self):
        self.next_token()
        if self.token.kind == TokenType.CONST_NUMERIC:
            result = self.parse_integer(self.token.text)
        else:
            raise Exception('syntax error: unexpected token')

        return result

    def expect_token(self, token_type):
        self.next_token()
        if self.token.kind != token_type:
            raise Exception('unexpected token')

    def parse_struct(self):
        item = StructDef()
        item.name = self.parse_name_token()
        self.expect_token(TokenType.OP_LEFT_BRACE)

        while True:
            next_token = self.peek_next_token()
            if next_token:
                if next_token.kind == TokenType.OP_RIGHT_BRACE:
                    break
            else:
                break

            child = self.parse_struct_item()
            if child:
                item.add(child)
            else:
                break

        self.expect_token(TokenType.OP_RIGHT_BRACE)
        return item

    def parse_enum(self):
        item = EnumDef()
        item.name = self.parse_name_token()
        self.expect_token(TokenType.OP_LEFT_BRACE)

        while True:
            next_token = self.lexer.peek_token()
            if next_token:
                if next_token.kind == TokenType.OP_RIGHT_BRACE:
                    # skip next token
                    self.next_token()
                    break
            else:
                break

            child = self.parse_enum_item()
            if child:
                item.add(child)
            else:
                break

        return item

    def parse_enum_item(self):
        item = EnumItemDef()
        item.name = self.parse_name_token()

        while True:
            self.next_token()

            if self.token:
                # optional assignment to a value
                if self.token.kind == TokenType.OP_ASSIGN:
                    item.key = self.parse_integer_token()
                elif self.token.kind == TokenType.OP_LEFT_BRACKET:
                    item.properties = self.parse_property_list()
                elif self.token.kind == TokenType.OP_COMMA:
                    break
                elif self.token.kind == TokenType.OP_END_OF_STATEMENT:
                    break
                else:
                    raise Exception('unexpected token')
            else:
                raise Exception('syntax error: missing token')

        return item

    def parse_struct_item(self):
        item = StructItemDef()

        # Data type first
        item.data_type = self.parse_name_token()

        # Check for optional array specifier

        next_token = self.peek_next_token()
        if next_token.kind == TokenType.OP_LEFT_BRACKET:
            self.next_token()
            # this is an array
            item.dim = self.parse_integer_token()
            self.expect_token(TokenType.OP_RIGHT_BRACKET)

        # item identifier
        item.name = self.parse_name_token()

        # check for optional properties and end of statement
        while True:
            next_token = self.peek_next_token()

            if next_token:
                # optional assignment to a value
                if next_token.kind == TokenType.OP_LEFT_BRACKET:
                    self.next_token()
                    item.properties = self.parse_property_list()
                elif next_token.kind == TokenType.OP_END_OF_STATEMENT:
                    self.next_token()
                    break
                else:
                    raise Exception('unexpected token')
            else:
                raise Exception('syntax error: missing token')

        return item

    def parse_property_list(self):
        result = PropertyList()

        while True:
            self.next_token()
            if self.token.kind == TokenType.OP_RIGHT_BRACKET:
                break
            elif self.token.kind == TokenType.VALUE:
                property_name = self.token.text
                self.expect_token(TokenType.OP_ASSIGN)
                self.next_token()
                if self.token.kind == TokenType.VALUE or self.token.kind == TokenType.CONST_STRING or self.token.kind == TokenType.CONST_NUMERIC:
                    result.add_property(property_name, self.token.text, self.token.kind)
                else:
                    raise Exception('unexpected token')

                self.next_token()
                if self.token.kind == TokenType.OP_COMMA:
                    pass
                elif self.token.kind == TokenType.OP_RIGHT_BRACKET:
                    break
                else:
                    raise Exception('syntax error')
            else:
                raise Exception('syntax error: unexpected token')

        return result
