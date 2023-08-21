from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    VAR = 0
    LPAR = 1
    RPAR = 2

    PLUS = 3,
    MINUS = 4,
    MULTIPLY = 5,
    DIVIDE = 6,
    ASSIGN = 7,
    EQUALS = 8
    NOT = 9

    KEYWORD_PRINT = 10
    KEYWORD_INPUT = 11

    KEYWORD_HALT = 12
    KEYWORD_IF = 13
    KEYWORD_ELSE = 14

    BLOCK_START = 15
    BLOCK_END = 16

    NUM = 17


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int


class Lexer:
    def __init__(self, code):
        self.code = code
        self.start = 0
        self.current = 0
        self.current_line = 1

        self.tokens = []

    def add_token(self, token_type):
        self.tokens.append(Token(token_type,
                                 self.code[self.start:self.current],
                                 self.current_line))

    def reached_end(self) -> bool:
        return self.current >= len(self.code)

    def next(self) -> None | str:
        if self.reached_end():
            return None
        self.current += 1
        return self.code[self.current - 1]

    def peek(self) -> None | str:
        if self.reached_end():
            return None
        return self.code[self.current]

    def peek_next(self) -> None | str:
        if self.current + 1 >= len(self.code):
            return None
        return self.code[self.current + 1]

    def match(self, expected) -> bool:
        if self.reached_end():
            return False
        if self.code[self.current] != expected:
            return False
        self.next()
        return True

    def scan(self) -> list[Token]:
        while not self.reached_end():
            self.start = self.current
            self.scan_token()
        return self.tokens

    def scan_token(self):
        char: str = self.next()
        if char == "(":
            self.add_token(TokenType.LPAR)
        elif char == ")":
            self.add_token(TokenType.RPAR)
        elif char == "{":
            self.add_token(TokenType.BLOCK_START)
        elif char == "}":
            self.add_token(TokenType.BLOCK_END)
        elif char == "+":
            self.add_token(TokenType.PLUS)
        elif char == "-":
            self.add_token(TokenType.MINUS)
        elif char == "*":
            self.add_token(TokenType.MULTIPLY)
        elif char == "/":
            self.add_token(TokenType.DIVIDE)
        elif char == "=":
            if self.match("="):
                self.add_token(TokenType.EQUALS)
            else:
                self.add_token(TokenType.ASSIGN)
        elif char == "!":
            self.add_token(TokenType.NOT)
        elif char == "\n":
            self.current_line += 1
        elif char == " " or char == "\t":
            pass
        else:
            if char.isnumeric():
                self.scan_number()
            elif char.isalpha():
                self.scan_identifier()
            else:
                raise ValueError(f"Invalid syntax at line {self.current_line}")

    def scan_number(self):
        while not self.reached_end() and self.peek().isnumeric():
            self.next()

        if self.peek() == "." and self.peek().isnumeric():
            self.next()
            while not self.reached_end() and self.peek().isnumeric():
                self.next()

        self.add_token(TokenType.NUM)

    def scan_identifier(self):
        while not self.reached_end() and self.peek().isalnum():
            self.next()

        text = self.code[self.start:self.current]

        if text == "if":
            self.add_token(TokenType.KEYWORD_IF)
        elif text == "else":
            self.add_token(TokenType.KEYWORD_ELSE)
        elif text == "print":
            self.add_token(TokenType.KEYWORD_PRINT)
        elif text == "input":
            self.add_token(TokenType.KEYWORD_INPUT)
        elif text == "halt":
            self.add_token(TokenType.KEYWORD_HALT)
        else:
            self.add_token(TokenType.VAR)
