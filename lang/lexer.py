import re
import sys

from utils.token import Token
from utils.tokentype import TokenType

class Lexer:
    def __init__(self, program):
        self.program = program
        self.line = 1
        self.grammar = None
        self.__load_grammar()

    def __load_grammar(self):
        try:
            with open("lang/tokenizer.g", 'r') as file:
                self.grammar = file.read()
        except FileNotFoundError:
            print("[ERROR] fault at core ( code: GRR )")
            sys.exit(1)

    def tokenize(self):
        token_list = list()
        compiled_grammar = re.compile(self.grammar, re.VERBOSE)
        for chunk in compiled_grammar.finditer(self.program):
            chunk = chunk.groupdict()
            token = self.get_token(chunk)
            if token is None: continue
            token_list.append(token)
        return token_list

    def get_token(self, chunk):
        if chunk['COMMENT'] is not None:
            return None
        elif chunk['NEWLINE'] is not None:
            self.line += 1
            return None
        elif chunk['STRING'] is not None:
            return Token(chunk['STRING'], TokenType.STRING, self.line)
        elif chunk['INTEGER'] is not None:
            return Token(chunk['INTEGER'], TokenType.INTEGER, self.line)
        elif chunk['OPERATOR'] is not None:
            return self.get_token_operator(chunk['OPERATOR'])
        elif chunk['IDENTIFIER'] is not None:
            return self.get_token_identifier(chunk['IDENTIFIER'])
        print(chunk)
        print("[ERROR] fault at core ( code: TTY )")
        sys.exit(1)

    def get_token_operator(self, raw_chunk):
        if raw_chunk == '(':
            return Token(raw_chunk, TokenType.OPEN_PARAM, self.line)
        elif raw_chunk == ')':
            return Token(raw_chunk, TokenType.CLOSE_PARAM, self.line)
        elif raw_chunk == '{':
            return Token(raw_chunk, TokenType.OPEN_BRACE, self.line)
        elif raw_chunk == '}':
            return Token(raw_chunk, TokenType.CLOSE_BRACE, self.line)
        elif raw_chunk == ';':
            return Token(raw_chunk, TokenType.SEMICOLON, self.line)
        elif raw_chunk == '!':
            return Token(raw_chunk, TokenType.NOT, self.line)
        elif raw_chunk == '+':
            return Token(raw_chunk, TokenType.PLUS, self.line)
        elif raw_chunk == '-':
            return Token(raw_chunk, TokenType.MINUS, self.line)
        elif raw_chunk == '*':
            return Token(raw_chunk, TokenType.STAR, self.line)
        elif raw_chunk == '/':
            return Token(raw_chunk, TokenType.SLASH, self.line)
        elif raw_chunk == '>':
            return Token(raw_chunk, TokenType.GREATER, self.line)
        elif raw_chunk == '<':
            return Token(raw_chunk, TokenType.LESSER, self.line)
        elif raw_chunk == '>=':
            return Token(raw_chunk, TokenType.GREATER_EQUAL, self.line)
        elif raw_chunk == '<=':
            return Token(raw_chunk, TokenType.LESSER_EQUAL, self.line)
        elif raw_chunk == '==':
            return Token(raw_chunk, TokenType.EQUAL_EQUAL, self.line)
        elif raw_chunk == '!=':
            return Token(raw_chunk, TokenType.BANG_EQUAL, self.line)
        print("[ERROR] fault at core ( code: TTO )")
        sys.exit(1)

    def get_token_identifier(self, raw_chunk):
        if raw_chunk == 'define':
            return Token(raw_chunk, TokenType.KW_DEFINE, self.line)
        elif raw_chunk == 'return':
            return Token(raw_chunk, TokenType.KW_RETURN, self.line)
        else:
            return Token(raw_chunk, TokenType.ID, self.line)