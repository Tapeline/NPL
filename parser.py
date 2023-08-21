from lexer import TokenType
from nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def reached_end(self):
        return self.current >= len(self.tokens)

    def next(self):
        if self.reached_end():
            return None
        self.current += 1
        return self.tokens[self.current - 1]

    def peek(self):
        if self.reached_end():
            return None
        return self.tokens[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.tokens):
            return None
        return self.tokens[self.current + 1]

    def previous(self):
        if self.current == 0:
            return None
        return self.tokens[self.current - 1]

    def match(self, expected_type):
        if self.reached_end():
            return None
        if self.tokens[self.current].type != expected_type:
            return None
        return self.next()

    def require(self, expected_type):
        token = self.match(expected_type)
        if token is None:
            raise ValueError(f"Expected {expected_type} but got {self.peek().type} "
                             f"at line {self.peek().line}")
        return token

    def parse(self):
        nodes = []
        while not self.reached_end():
            nodes.append(self.parse_statement())
        return BlockNode(None, nodes)

    def parse_statement(self):
        if self.match(TokenType.BLOCK_START) is not None:
            token = self.previous()
            nodes = []
            while self.match(TokenType.BLOCK_END) is None:
                nodes.append(self.parse_statement())
            return BlockNode(token, nodes)

        elif self.match(TokenType.KEYWORD_IF) is not None:
            token = self.previous()
            condition = self.parse_expression()
            if_code = self.parse_statement()
            else_code = None
            if self.match(TokenType.KEYWORD_ELSE) is not None:
                else_code = self.parse_statement()
            return IfNode(token, condition, if_code, else_code)

        elif self.match(TokenType.KEYWORD_HALT) is not None:
            return HaltNode(self.previous())

        else:
            return self.parse_expression()

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        left = self.parse_equality()
        if self.match(TokenType.ASSIGN) is not None:
            token = self.previous()
            value = self.parse_assignment()
            return AssignNode(token, left.name, value)
        return left

    def parse_equality(self):
        left = self.parse_term()
        while self.match(TokenType.EQUALS) is not None:
            token = self.previous()
            left = BinaryOperatorNode(token, left, self.parse_term())
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.match(TokenType.PLUS) is not None or \
                self.match(TokenType.MINUS) is not None:
            token = self.previous()
            left = BinaryOperatorNode(token, left, self.parse_factor())
        return left

    def parse_factor(self):
        left = self.parse_unary()
        while self.match(TokenType.MULTIPLY) is not None or \
                self.match(TokenType.DIVIDE) is not None:
            token = self.previous()
            left = BinaryOperatorNode(token, left, self.parse_unary())
        return left

    def parse_unary(self):
        if self.match(TokenType.NOT) is not None:
            return UnaryOperatorNode(self.previous(), self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        if self.match(TokenType.LPAR) is not None:
            expr = self.parse_expression()
            self.require(TokenType.RPAR)
            return expr
        elif self.match(TokenType.KEYWORD_PRINT) is not None:
            return PrintNode(self.previous(), self.parse_expression())
        elif self.match(TokenType.KEYWORD_INPUT) is not None:
            return InputNode(self.previous())
        elif self.match(TokenType.NUM) is not None:
            return NumNode(self.previous())
        elif self.match(TokenType.VAR) is not None:
            return VarNode(self.previous())
        else:
            raise ValueError(f"Unparsable expression at line {self.peek().line}")
