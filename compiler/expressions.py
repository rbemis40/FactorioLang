from compiler.core import State
from enum import Enum

# TODO: Avoid redefining this in statements.py
class ExpOp (Enum):
    ADD = 1,
    SUB = 2,
    MUL = 3,
    DIV = 4,
    MOD = 5

class Expression:
    def get_value(self, state: State) -> int:
        return 0 # TODO: PLACEHOLDER

class SingleValExpression (Expression):
    def __init__(self, val: int):
        self.val = val

    def get_value(self, state: State) -> int:
        return self.val
    
class ExpressionTree (Expression):
    def __init__(self, operation: ExpOp, left_exp: Expression, right_exp: Expression):
        self.left_exp = left_exp
        self.right_exp = right_exp
        self.operation = operation

    def get_value(self, state: State):
        pass 