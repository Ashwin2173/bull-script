from enum import Enum, auto

class StatementType(Enum):
    EXPRESSION_STATEMENT = auto()

    UNARY_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()

    ID = auto()
    INTEGER_LITERAL = auto()
    STRING_LITERAL = auto()
    DOUBLE_LITERAL = auto()

    RETURN_STATEMENT = auto()
    FUNCTION_DECLARATION = auto()
    VARIABLE_EXPRESSION = auto()
