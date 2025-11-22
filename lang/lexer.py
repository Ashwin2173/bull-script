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
        elif chunk['FLOAT'] is not None:
            return Token(chunk['FLOAT'], TokenType.DOUBLE, self.line)
        elif chunk['OPERATOR'] is not None:
            return self.get_token_operator(chunk['OPERATOR'])
        elif chunk['IDENTIFIER'] is not None:
            return self.get_token_identifier(chunk['IDENTIFIER'])
        print("[ERROR] fault at core ( code: TTY )")
        sys.exit(1)

    def get_token_operator(self, raw_chunk):
        token_map = {
            '(': TokenType.OPEN_PARAM,
            ')': TokenType.CLOSE_PARAM,
            '{': TokenType.OPEN_BRACE,
            '}': TokenType.CLOSE_BRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '!': TokenType.NOT,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '>': TokenType.GREATER,
            '<': TokenType.LESSER,
            '=': TokenType.EQUAL,
            '>=': TokenType.GREATER_EQUAL,
            '<=': TokenType.LESSER_EQUAL,
            '==': TokenType.EQUAL_EQUAL,
            '!=': TokenType.BANG_EQUAL,
        }
        token_type = token_map.get(raw_chunk)
        if token_type is None:
            print("[ERROR] fault at core ( code: TTO )")
            sys.exit(1)
        return Token(raw_chunk, token_type, self.line)

    def get_token_identifier(self, raw_chunk):
        keyword_map = {
            'define': TokenType.KW_DEFINE,
            'return': TokenType.KW_RETURN,
            'true': TokenType.KW_TRUE,
            'false': TokenType.KW_FALSE,
            'var': TokenType.KW_VAR,
            'if': TokenType.KW_IF,
            'while': TokenType.KW_WHILE
        }
        keyword_type = keyword_map.get(raw_chunk)
        if keyword_type is not None:
            return Token(raw_chunk, keyword_type, self.line)
        else:
            return Token(raw_chunk, TokenType.ID, self.line)