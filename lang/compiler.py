import sys
from xml.dom.pulldom import START_ELEMENT

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
        for statement in definition.get_body():
            if statement.get_type() == StatementType.RETURN_STATEMENT:
                self.__process_return_statement(statement)
            elif statement.get_type() == StatementType.VARIABLE_EXPRESSION:
                self.__process_variable_declaration(statement)
            elif statement.get_type() == StatementType.EXPRESSION_STATEMENT:
                self.builder.add(self.__process_expression(statement))
                self.builder.add(";")
            else:
                print("[ERROR] unhandled statement")
                sys.exit(1)
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
        elif expression.get_type() in {StatementType.INTEGER_LITERAL, StatementType.STRING_LITERAL,
                                       StatementType.DOUBLE_LITERAL, StatementType.ID}:
            return self.__process_literal(expression)
        elif expression.get_type() == StatementType.BINARY_EXPRESSION:
            return self.__process_binary_statement(expression)
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
        }
        return (self.__process_expression(expression.get_left()) +
                operation_map[expression.get_operation()] + "(" +
                self.__process_expression(expression.get_right()) + ")")

    def __process_literal(self, expression):
        if expression.get_type() == StatementType.INTEGER_LITERAL:
            return f"(new Integer({expression.get_value()}LL))"
        elif expression.get_type() == StatementType.STRING_LITERAL:
            return f"(new String({expression.get_value()}))"
        elif expression.get_type() == StatementType.DOUBLE_LITERAL:
            return f"(new Double({expression.get_value()}L))"
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
        self.builder.add(default.DEFAULT_TYPE_POST_FUNCTION)
        self.builder.add(default.DEFAULT_FUNCTIONS)

    def __add_default_tracked(self):
        for item in self.defaults_tracker:
            if item == StatementType.INTEGER_LITERAL:
                self.builder.add(default.INTEGER)
