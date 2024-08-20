from compiler.core import State, Translatable, Instruction
from enum import Enum
from abc import ABC, abstractmethod

# TODO: Avoid redefining this in statements.py
class ExpOp (Enum):
    ADD = 1,
    SUB = 2,
    MUL = 3,
    DIV = 4,
    MOD = 5

class Expression (Translatable):
    @abstractmethod
    def is_computable() -> bool:
        pass

    @abstractmethod
    def get_value() -> int:
        pass

class SingleValExpression (Expression):
    def __init__(self, val: int):
        self.val = val

    def translate(self, state: State) -> list[Instruction]:
        return [] # TODO: Implement

    def is_computable(self) -> bool:
        return True

    def get_value(self) -> int:
        return self.val
    
class ExpressionTree (Expression):
    def __init__(self, operation: ExpOp, left_exp: Expression, right_exp: Expression):
        self.left_exp = left_exp
        self.right_exp = right_exp
        self.operation = operation

    def translate(self, state: State) -> list[Instruction]:
        return [] # TODO: Implement

    def is_computable(self) -> bool:
        return self.left_exp.is_computable() and self.right_exp.is_computable()

    def get_value(self, state: State):
        pass