import sys
import enum
import re


class Lexer:
    STATE_UNKNOWN = 0
    STATE_NORMAL = 1
    STATE_QUOTED = 2
    STATE_ELEMENT = 3
    STATE_LINECOMMENT = 4
    STATE_BLOCKCOMMENT = 5


    def __init__(self, input_data):
        self.data = input_data
        self.total_length = len(self.data)
        self.state = self.STATE_NORMAL
        self.index = 0

        self.keywords = []

        self.special_characters = [
            '=', '[', ']', '{', '}', ';', ','
        ]

        self.operators = {
            '=': TokenType.OP_ASSIGN,
            '[': TokenType.OP_LEFT_BRACKET,
            ']': TokenType.OP_RIGHT_BRACKET,
            ';': TokenType.OP_END_OF_STATEMENT,
            '{': TokenType.OP_LEFT_BRACE,
            '}': TokenType.OP_RIGHT_BRACE,
            ',': TokenType.OP_COMMA
        }

        self.hex_regex = re.compile('^0[xX][0-9a-fA-F]+$')
        self.binary_regex = re.compile('^0[bB][0-1]+$')
        self.number_regex = re.compile('^\\d+\\.?\\d*$')

    def get_next_character(self):
        result = None
        if self.index < self.total_length:
            result = self.data[self.index]
            self.index += 1

        return result

    def push_back_character(self):
        if self.index > 0:
            self.index -= 1

    def peek_next_character(self):
        result = None
        if self.index < self.total_length:
            result = self.data[self.index]

        return result

    def peek_token(self):
        saved_index = self.index
        saved_state = self.state
        result = self.get_token()
        self.index = saved_index
        self.state = saved_state
        return result

    def get_token(self):
        result = None
        value = ''

        while True:
            c = self.get_next_character()

            if self.state == self.STATE_QUOTED:
                if c:
                    if c == '"':
                        # end of string; add the token
                        self.state = self.STATE_NORMAL
                        result = Token(value, TokenType.CONST_STRING)
                        break
                    else:
                        value += c
                else:
                    # no further characters
                    raise Exception('syntax error: string missing end quote')

            elif self.state == self.STATE_NORMAL:
                if c:
                    next_char = self.peek_next_character()
                    if c.isspace():
                        # ignore normal whitespace
                        pass
                    elif c == '/' and next_char == '/':
                        self.state = self.STATE_LINECOMMENT
                        value = ''
                    elif c == '/' and next_char == '*':
                        self.state = self.STATE_BLOCKCOMMENT
                        value = ''
                    elif c == '#':
                        self.state = self.STATE_LINECOMMENT
                        value = ''
                    elif c in self.special_characters:
                        result = self.evaluate_operator_value(c)
                        self.state = self.STATE_NORMAL
                        break
                    else:
                        value = c
                        self.state = self.STATE_ELEMENT
                else:
                    # no further characters... we are done
                    break

            elif self.state == self.STATE_ELEMENT:
                if c:
                    if c.isspace():
                        # end element
                        self.state = self.STATE_NORMAL
                        if value:
                            result = self.evaluate_token_value(value)
                            break
                    elif c in self.special_characters:
                        # end element
                        self.state = self.STATE_NORMAL
                        self.push_back_character()
                        if value:
                            result = self.evaluate_token_value(value)
                            break
                    else:
                        value += c
                else:
                    # no further characters... end element
                    result = self.evaluate_token_value(value)
                    break

            elif self.state == self.STATE_LINECOMMENT:
                if c:
                    if c == '\n' :
                        self.state = self.STATE_NORMAL
                        value = ''
                else:
                    break

            elif self.state == self.STATE_BLOCKCOMMENT:
                if c:
                    next_char = self.peek_next_character()
                    if c == '*' and next_char == '/':
                        self.get_next_character()
                        self.state = self.STATE_NORMAL
                        value = ''
                else:
                    break

            else:
                raise Exception('unknown state')

        return result

    def evaluate_token_value(self, value):
        if value:
            if value in self.keywords:
                result = Token(value, TokenType.KEYWORD)
            elif value in self.operators:
                result = Token(value, self.operators[value])
            else:
                if self.is_numeric(value):
                    result = Token(value, TokenType.CONST_NUMERIC)
                else:
                    result = Token(value, TokenType.VALUE)
        else:
            raise Exception('invalid token value')

        return result

    def evaluate_operator_value(self, value):
        if value:
            if value in self.operators:
                result = Token(value, self.operators[value])
            else:
                raise Exception('invalid operator')
        else:
            raise Exception('invalid token')

        return result

    def is_numeric(self, value):
        return self.number_regex.match(value) or self.hex_regex.match(value) or self.binary_regex.match(value)


class Token:
    def __init__(self, token_text, token_type):
        self.text = token_text   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = token_type   # The TokenType that this token is classified as.


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    KEYWORD = 0
    CONST_STRING = 1
    CONST_NUMERIC = 2
    VALUE = 3
    OP_ASSIGN = 100
    OP_LEFT_BRACKET = 101
    OP_RIGHT_BRACKET = 102
    OP_END_OF_STATEMENT = 103
    OP_LEFT_BRACE = 104,
    OP_RIGHT_BRACE = 105
    OP_COMMA = 106
