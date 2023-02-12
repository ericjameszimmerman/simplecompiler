from generator import Lexer
from generator import Parser
from generator import SyntaxTree

def cli_main():
    filename = "D:\\Projects\\lexer\\test1.dmod"
    data = None

    with open(filename) as f:
        data = f.read()

    lexer = Lexer(data)
    data = SyntaxTree()
    parser = Parser(lexer, data)
    parser.parse()
    print(data)


if __name__ == '__main__':
    cli_main()
