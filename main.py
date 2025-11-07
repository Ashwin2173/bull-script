import sys

from lang.lexer import Lexer
from lang.parser import Parser

def print_usage():
    print("USAGE: ")
    print("    luna *.luna")
    sys.exit(1)

# todo: fix this
def main(args):
    if len(args) < 2:
        print_usage()
    raw_program = None
    try:
        with open(args[1], 'r') as file:
            raw_program = file.read()
    except FileNotFoundError:
        print("[ERROR] file not found")
        print_usage()
    transpile(raw_program)

def transpile(program):
    lexer = Lexer(program)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    print(parser.parse())

if __name__ == "__main__":
    main(sys.argv)
