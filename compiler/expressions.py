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
    def __init__(self):
        self.ans_loc: int = 0 # This will be used to store the memory location of the expressions answer for use in other expressions, 0 for placeholder
    
    @abstractmethod
    def is_computable() -> bool:
        pass

    @abstractmethod
    def get_value() -> int:
        pass

    def get_ans_loc(self) -> int:
        return self.ans_loc

class SingleValExpression (Expression):
    def __init__(self, val: int):
        self.val = val

    def translate(self, state: State) -> list[Instruction]:
        return [] # TODO: Implement

    def is_computable(self) -> bool:
        return True

    def get_value(self) -> int:
        return self.val
    
class TreeExpression (Expression):
    def __init__(self, operation: ExpOp, left_exp: Expression, right_exp: Expression):
        self.left_exp = left_exp
        self.right_exp = right_exp
        self.operation = operation

    def translate(self, state: State) -> list[Instruction]:
        return [] # TODO: Implement

    def is_computable(self) -> bool:
        return self.left_exp.is_computable() and self.right_exp.is_computable()

    def get_value(self) -> int:
        if not self.is_computable():
            raise ValueError('Attempted to get value of non-computable expression')

        left_val = self.left_exp.get_value()
        right_val = self.right_exp.get_value()

        match self.operation:
            case ExpOp.ADD:
                return left_val + right_val
            case ExpOp.SUB:
                return left_val - right_val
            case ExpOp.MUL:
                return left_val * right_val
            case ExpOp.DIV:
                return left_val // right_val
            case ExpOp.MOD:
                return left_val % right_val
            case _:
                raise Exception('Unknown expression type')