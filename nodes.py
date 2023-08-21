class Node:
    def __init__(self, token):
        self.token = token


class VarNode(Node):
    def __init__(self, token):
        super().__init__(token)
        self.name = token.lexeme


class NumNode(Node):
    def __init__(self, token):
        super().__init__(token)
        self.value = float(token.lexeme)


class PrintNode(Node):
    def __init__(self, token, value):
        super().__init__(token)
        self.value = value


class InputNode(Node):
    pass


class HaltNode(Node):
    pass


class BinaryOperatorNode(Node):
    def __init__(self, token, left, right):
        super().__init__(token)
        self.left = left
        self.right = right


class AssignNode(Node):
    def __init__(self, token, var, value):
        super().__init__(token)
        self.var = var
        self.value = value


class UnaryOperatorNode(Node):
    def __init__(self, token, right):
        super().__init__(token)
        self.right = right


class BlockNode(Node):
    def __init__(self, token, nodes):
        super().__init__(token)
        self.nodes = nodes


class IfNode(Node):
    def __init__(self, token, condition, if_block, else_block):
        super().__init__(token)
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block
