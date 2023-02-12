from .lexer import Lexer
from .lexer import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.keywords = [
            'enum',
            'struct'
        ]

        self.subparsers = {
            'enum': self.parse_enum,
            'struct': self.parse_struct,
        }

    def parse(self):
        self.lexer.keywords = self.keywords

        while True:
            token = self.lexer.get_token()
            if token:
                if token.kind == TokenType.KEYWORD:
                    if token.text in self.subparsers:
                        self.subparsers[token.text]()
                else:
                    raise Exception('syntax error')
            else:
                break


    def parse_struct(self):
        pass

    def parse_enum(self):
        enum_name = self.lexer.get_token()
        pass
