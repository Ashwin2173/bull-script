from enum import Enum, auto

class TokenType(Enum):
    ID = auto()
    STRING = auto()
    INTEGER = auto()
    DOUBLE = auto()

    OPEN_PARAM = auto()
    CLOSE_PARAM = auto()
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LESSER = auto()
    GREATER = auto()
    EQUAL = auto()
    PLUS_EQUAL = auto()
    MINUS_EQUAL = auto()
    LESSER_EQUAL = auto()
    GREATER_EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    KW_DEFINE = auto()
    KW_RETURN = auto()
    KW_TRUE = auto()
    KW_FALSE = auto()
    KW_VAR = auto()

def to_string(token_type):
    for attr in dir(TokenType):
        if getattr(TokenType, attr) == token_type:
            return attr
    return None