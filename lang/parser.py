import sys
from token import tok_name

from utils.generator import Generator
from utils.tokentype import TokenType, to_string
from utils.statement_type import StatementType
from lang.exceptions import BullException
from utils.models import *

class Parser:
    def __init__(self, tokens):
        self.tokens = Generator(tokens)

    def parse(self):
        definition = list()
        while self.tokens.has_next():
            token = self.tokens.get()
            if token.get_type() == TokenType.KW_DEFINE:
                definition.append(self.__parse_function())
            else:
                print("[ERROR] Invalid token:", to_string(token.get_type()))
                sys.exit(1)
            self.tokens.next()
        return Program(definition)

    def __parse_statement(self):
        token = self.tokens.get()
        if token.get_type() == TokenType.KW_RETURN:
            statement = self.__return_statement()
            self.tokens.get().match(TokenType.SEMICOLON)
            return statement
        elif token.get_type() == TokenType.KW_VAR:
            statement = self.__var_statement()
            self.tokens.get().match(TokenType.SEMICOLON)
            return statement
        else:
            expression = self.__expression()
            self.tokens.get().match(TokenType.SEMICOLON)
            return expression

    def __parse_function(self):
        function_name = self.tokens.next().match(TokenType.ID)
        self.tokens.next().match(TokenType.OPEN_PARAM)
        self.tokens.next().match(TokenType.CLOSE_PARAM)
        self.tokens.next()
        function_block = self.__parse_block()
        return FunctionDeclaration(function_name.get_raw(), function_block,
                                   StatementType.FUNCTION_DECLARATION, function_name.get_line())

    def __parse_block(self):
        statement = list()
        self.tokens.get().match(TokenType.OPEN_BRACE)
        while self.tokens.has_next():
            self.tokens.next()
            if self.tokens.get() == TokenType.CLOSE_BRACE: break
            statement.append(self.__parse_statement())
        self.tokens.get().match(TokenType.CLOSE_BRACE)
        return statement

    def __var_statement(self):
        self.tokens.next()
        name = self.tokens.get()
        self.tokens.next().match(TokenType.EQUAL)
        self.tokens.next()
        expression = self.__logical_or()
        return VariableDeclaration(name.get_raw(), expression, StatementType.VARIABLE_EXPRESSION, name.get_line())

    def __return_statement(self):
        self.tokens.next()
        expression = self.__expression()
        return ReturnStatement(expression, StatementType.RETURN_STATEMENT, expression.get_line())

    def __expression(self):
        return Expression(self.__assignment(), StatementType.EXPRESSION_STATEMENT,
            self.tokens.get().get_line())

    def __assignment(self):
        left_expression = self.__logical_or()
        while self.tokens.get().contains(TokenType.EQUAL, TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__logical_or()
            if left_expression.get_type() != StatementType.ID:
                raise BullException("cannot assign to an expression")
            left_expression = BinaryExpression(left_expression, token.get_raw(),
                                    right_expression, StatementType.BINARY_EXPRESSION, token.get_line())
        return left_expression

    def __logical_or(self):
        left_expression = self.__logical_and()
        while self.tokens.get().contains(TokenType.OR):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__logical_and()
            left_expression = BinaryExpression(left_expression, token.get_raw(),
                                    right_expression, StatementType.BINARY_EXPRESSION, token.get_line())
        return left_expression

    def __logical_and(self):
        left_expression = self.__equality()
        while self.tokens.get().contains(TokenType.AND):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__equality()
            left_expression = BinaryExpression(left_expression, token.get_raw(),
                                    right_expression, StatementType.BINARY_EXPRESSION, token.get_line())
        return left_expression

    def __equality(self):
        left_expression = self.__comparison()
        while self.tokens.get().contains(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__comparison()
            left_expression = BinaryExpression(left_expression, token.get_type(),
                                    right_expression, StatementType.BINARY_EXPRESSION, token.get_line())
        return left_expression

    def __comparison(self):
        left_expression = self.__term()
        while self.tokens.get().contains(TokenType.LESSER, TokenType.GREATER,
                                      TokenType.LESSER_EQUAL, TokenType.GREATER_EQUAL):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__term()
            left_expression = BinaryExpression(left_expression, token.get_type(),
                                    right_expression, StatementType.BINARY_EXPRESSION, token.get_line())
        return left_expression

    def __term(self):
        left_expression = self.__factor()
        while self.tokens.get().contains(TokenType.PLUS, TokenType.MINUS):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__factor()
            left_expression = BinaryExpression(left_expression, token.get_type(),
                                    right_expression, StatementType.BINARY_EXPRESSION, token.get_line())
        return left_expression

    def __factor(self):
        left_expression = self.__unary()
        while self.tokens.get().contains(TokenType.STAR, TokenType.SLASH):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__unary()
            left_expression = BinaryExpression(left_expression, token.get_type(),
                                    right_expression, StatementType.BINARY_EXPRESSION,
                                    token.get_line())
        return left_expression

    def __unary(self):
        if self.tokens.get().contains(TokenType.NOT, TokenType.MINUS):
            token = self.tokens.get()
            self.tokens.next()
            right_expression = self.__unary()
            return Unary(token.get_type(), right_expression,
                         StatementType.UNARY_EXPRESSION, token.get_line())
        return self.__primary()

    def __primary(self):
        token = self.tokens.get()
        self.tokens.next()
        if token == TokenType.INTEGER:
            return Literal(token.get_raw(), StatementType.INTEGER_LITERAL, token.get_line())
        elif token == TokenType.STRING:
            return Literal(token.get_raw(), StatementType.STRING_LITERAL, token.get_line())
        elif token == TokenType.DOUBLE:
            return Literal(token.get_raw(), StatementType.DOUBLE_LITERAL, token.get_line())
        elif token == TokenType.KW_TRUE or token == TokenType.KW_FALSE:
            return Literal(token.get_raw(), StatementType.BOOLEAN_LITERAL, token.get_line())
        elif token == TokenType.ID:
            next_token = self.tokens.get()
            if next_token == TokenType.OPEN_PARAM:
                return FunctionCall(token.get_raw(), self.__parse_function_param(),
                                    StatementType.FUNCTION_CALL, token.get_line())
            return Literal(token.get_raw(), StatementType.ID, token.get_line())
        else:
            raise BullException("Invalid expression, " + token.get_raw())

    def __parse_function_param(self):
        param = list()
        self.tokens.next()
        while not self.tokens.get().contains(TokenType.CLOSE_PARAM):
            param.append(self.__logical_or())
            if not self.tokens.get().contains(TokenType.CLOSE_PARAM):
                self.tokens.get().match(TokenType.COMMA)
        self.tokens.next()
        return param
