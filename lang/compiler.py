import sys

from utils.builder import ProgramBuilder
from utils.statement_type import StatementType

import lang.default as default
from utils.tokentype import TokenType


class Compiler:
    def __init__(self, program):
        self.program = program
        self.builder = ProgramBuilder()
        self.defaults_tracker = set()
        self.__add_defaults()

    def compile(self):
        self.__process_program()
        self.builder.add(default.MAIN_FUNCTION)
        # self.__add_default_tracked()
        return self.builder

    def __process_program(self):
        self.__process_definitions()

    def __process_definitions(self):
        definitions = self.program.get_definitions()
        for definition in definitions:
            if definition.get_type() == StatementType.FUNCTION_DECLARATION:
                self.__process_function_declaration(definition)
            else:
                print("[ERROR] unhandled definition")
                sys.exit(1)

    def __process_function_declaration(self, definition):
        name = definition.get_name()
        name = "main_" if name == "main" else name
        self.builder.add(f"Object* {name}() {{")
        self.__process_statements(definition.get_body())
        self.builder.add("}")

    def __process_statements(self, statement_list):
        for statement in statement_list:
            if statement.get_type() == StatementType.RETURN_STATEMENT:
                self.__process_return_statement(statement)
            elif statement.get_type() == StatementType.VARIABLE_EXPRESSION:
                self.__process_variable_declaration(statement)
            elif statement.get_type() == StatementType.IF_STATEMENT:
                self.__process_if_statement(statement)
            elif statement.get_type() == StatementType.WHILE_STATEMENT:
                self.__process_while_statement(statement)
            elif statement.get_type() == StatementType.EXPRESSION_STATEMENT:
                self.builder.add(self.__process_expression(statement))
                self.builder.add(";")
            else:
                print("[ERROR] unhandled statement")
                sys.exit(1)

    def __process_while_statement(self, statement):
        self.builder.add("while(dynamic_cast<Boolean*>(")
        self.builder.add(self.__process_expression(statement.get_test()))
        self.builder.add(")->value){")
        self.__process_statements(statement.get_body())
        self.builder.add("}")

    def __process_if_statement(self, statement):
        self.builder.add("if(dynamic_cast<Boolean*>(")
        self.builder.add(self.__process_expression(statement.get_test()))
        self.builder.add(")->value){")
        self.__process_statements(statement.get_consequent())
        self.builder.add("}")

    def __process_variable_declaration(self, statement):
        self.builder.add("Object* ")
        self.builder.add(statement.get_name())
        self.builder.add("=")
        self.builder.add(self.__process_expression(statement.get_expression()))
        self.builder.add(";")

    def __process_return_statement(self, statement):
        self.builder.add("return ")
        self.builder.add(self.__process_expression(statement.get_expression()))
        self.builder.add(";")

    def __process_expression(self, expression):
        if expression.get_type() == StatementType.EXPRESSION_STATEMENT:
            return self.__process_expression(expression.get_expression())
        elif expression.get_type() in {StatementType.INTEGER_LITERAL, StatementType.STRING_LITERAL, StatementType.DOUBLE_LITERAL,
                                       StatementType.BOOLEAN_LITERAL, StatementType.ID}:
            return self.__process_literal(expression)
        elif expression.get_type() == StatementType.BINARY_EXPRESSION:
            return self.__process_binary_statement(expression)
        elif expression.get_type() == StatementType.UNARY_EXPRESSION:
            return self.__process_unary_statement(expression)
        elif expression.get_type() == StatementType.FUNCTION_CALL:
            return self.__process_function_call(expression)
        else:
            print("[ERROR] unhandled expression", expression.get_type())
            sys.exit(1)

    def __process_function_call(self, expression):
        name = expression.get_name()
        param = [self.__process_expression(p) for p in expression.get_param()]
        return f"{name}({', '.join(param)})"

    def __process_binary_statement(self, expression):
        operation_map = {
            TokenType.PLUS:  '->add',
            TokenType.MINUS: '->sub',
            TokenType.STAR:  '->mul',
            TokenType.SLASH: '->div',
            TokenType.GREATER: '->grt',
            TokenType.GREATER_EQUAL: '->gre',
            TokenType.LESSER: '->lsr',
            TokenType.LESSER_EQUAL: '->lse',
            TokenType.EQUAL_EQUAL: '->equals',
            TokenType.EQUAL: ' = '
        }
        return (self.__process_expression(expression.get_left()) +
                operation_map[expression.get_operation()] + "(" +
                self.__process_expression(expression.get_right()) + ")")

    def __process_unary_statement(self, expression):
        if expression.get_operator() == TokenType.MINUS:
            return f"({self.__process_expression(expression.get_right())}->negate())"
        else:
            print("0xDEAD")
            sys.exit(1)

    def __process_literal(self, expression):
        if expression.get_type() == StatementType.INTEGER_LITERAL:
            return f"get_int({expression.get_value()}LL)"
        elif expression.get_type() == StatementType.STRING_LITERAL:
            return f"get_string({expression.get_value()})"
        elif expression.get_type() == StatementType.DOUBLE_LITERAL:
            return f"get_double({expression.get_value()}L)"
        elif expression.get_type() == StatementType.BOOLEAN_LITERAL:
            return 'TRUE' if expression.get_value() == 'true' else 'FALSE'
        elif expression.get_type() == StatementType.ID:
            return expression.get_value()
        else:
            print("[ERROR] unhandled literal")
            sys.exit(1)

    def __add_defaults(self):
        for item in default.INCLUDES:
            self.builder.add("#include<" + item + ">\n")
        self.builder.add(default.OBJECT)
        self.builder.add(default.INTEGER)
        self.builder.add(default.STRING)
        self.builder.add(default.DOUBLE)
        self.builder.add(default.BOOLEAN)
        self.builder.add(default.DEFAULT_TYPE_POST_FUNCTION)
        self.builder.add(default.DEFAULT_FUNCTIONS)

    def __add_default_tracked(self):
        for item in self.defaults_tracker:
            if item == StatementType.INTEGER_LITERAL:
                self.builder.add(default.INTEGER)
