from lexer import Lexer
from parser import Parser
from runtime import Runtime


def main():
    with open("program.npl", "r") as file:
        code = file.read()
    lexer = Lexer(code)
    tokens = lexer.scan()
    parser = Parser(tokens)
    block = parser.parse()
    runtime = Runtime()
    runtime.run(block)


if __name__ == "__main__":
    main()
