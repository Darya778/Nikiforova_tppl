from .Token import Token


class Node:
    pass


class Number(Node):
    def __init__(self, token: Token) -> None:
        self.token = token

    def __str__(self) -> str:
        return f"{self.token}"


class BinOp(Node):

    def __init__(self, left: Node, op: Token, right: Node) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} {self.op.value} {self.right})"


class UnaryOp(Node):

    def __init__(self, op: Token, expr: Node) -> None:
        self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"({self.op}{self.expr})"


class Variable(Node):

    def __init__(self, name: Token):
        self.name = name

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.name})"


class Assignment(Node):

    def __init__(self, var: Token, expr: Node):
        self.var = var
        self.expr = expr

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.var} := {self.expr})"


class Statement(Node):

    def __init__(self, value: Node):
        self.value = value

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.value})"


class Empty(Node):

    def __init__(self):
        pass

    def __str__(self) -> str:
        return f"{__class__.__name__}"


class StatementList(Node):

    def __init__(self, first: Node, second: Node | None):
        self.first = first
        self.second = second

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.first}{f' SEMI {self.second}' if self.second is not None else ''})"


class ComplexStatement(Node):

    def __init__(self, list_: Node):
        self.list_ = list_

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.list_})"


class Program(Node):

    def __init__(self, comp_statement: Node):
        self.comp_statement = comp_statement

    def __str__(self) -> str:
        return f"{__class__.__name__}: {self.comp_statement}"
