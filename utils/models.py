class BaseClass:
    def __init__(self, _type, line):
        self._type = _type
        self.line = line

    def get_type(self):
        return self._type

    def get_line(self):
        return self.line

class Program:
    def __init__(self, definitions):
        self.definitions = definitions

    def get_definitions(self):
        return self.definitions
    
class Expression(BaseClass):
    def __init__(self, expression, _type, line):
        self.expression = expression
        super().__init__(_type, line)

    def get_expression(self):
        return self.expression

class BinaryExpression(BaseClass):
    def __init__(self, left, operator, right, _type, line):
        self.left = left
        self.operator = operator
        self.right = right
        super().__init__(_type, line)

    def get_left(self):
        return self.left

    def get_operation(self):
        return self.operator

    def get_right(self):
        return self.right

class Unary(BaseClass):
    def __init__(self, operator, right, _type, line):
        self.operator = operator
        self.right = right
        super().__init__(_type, line)

    def get_right(self):
        return self.right

class Literal(BaseClass):
    def __init__(self, value, _type, line):
        self.value = value
        super().__init__(_type, line)

    def get_value(self):
        return self.value

class ReturnStatement(BaseClass):
    def __init__(self, expression, _type, line):
        self.expression = expression
        super().__init__(_type, line)

    def get_expression(self):
        return self.expression

class FunctionDeclaration(BaseClass):
    def __init__(self, name, body, _type, line):
        self.name = name
        self.body = body
        super().__init__(_type, line)

    def get_name(self):
        return self.name

    def get_body(self):
        return self.body
