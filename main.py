from generator import Lexer


def cli_main():
    filename = "D:\\Projects\\lexer\\test1.dmod"
    data = None

    with open(filename) as f:
        data = f.read()

    lexer = Lexer(data)

    while True:
        token = lexer.get_token()
        if token:
            print(f'text = "{token.text}", kind = "{token.kind}"')
        else:
            break


if __name__ == '__main__':
    cli_main()
