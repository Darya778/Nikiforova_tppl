from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    VARIABLE = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    BEGIN = auto()
    END = auto()
    EQUAL = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    EOL = auto()


class Token:
    def __init__(self, type_: TokenType, value: str) -> None:
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f"({self.type_}: {self.value})"
