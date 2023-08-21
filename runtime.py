from nodes import *


class Runtime:
    def __init__(self):
        self.memory = {}

    def run(self, node):
        if isinstance(node, VarNode):
            if node.name not in self.memory:
                raise ValueError(f"Name {node.name} not defined")
            return self.memory[node.name]

        elif isinstance(node, NumNode):
            return node.value

        elif isinstance(node, PrintNode):
            print(self.run(node.value))

        elif isinstance(node, InputNode):
            return float(input("> "))

        elif isinstance(node, HaltNode):
            exit(0)

        elif isinstance(node, AssignNode):
            self.memory[node.var] = self.run(node.value)
            return self.memory[node.var]

        elif isinstance(node, BinaryOperatorNode):
            left = self.run(node.left)
            right = self.run(node.right)
            if node.token.lexeme == "+":
                return left + right
            elif node.token.lexeme == "-":
                return left - right
            elif node.token.lexeme == "*":
                return left * right
            elif node.token.lexeme == "/":
                return left / right
            elif node.token.lexeme == "==":
                return 1 if left == right else 0

        elif isinstance(node, UnaryOperatorNode):
            if node.token.lexeme == "!":
                value = self.run(node.right)
                return 0 if value == 1 else 1

        elif isinstance(node, BlockNode):
            for sub_node in node.nodes:
                self.run(sub_node)

        elif isinstance(node, IfNode):
            condition = self.run(node.condition)
            if condition == 1:
                self.run(node.if_block)
            else:
                if node.else_block is not Node:
                    self.run(node.else_block)
