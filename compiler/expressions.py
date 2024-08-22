from compiler.core import State, Translatable, Instruction
from compiler.instructions import SetInstruction, MathInstruction
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

    def set_ans_loc(self, new_loc: int) -> None:
        self.ans_loc = new_loc

    def get_ans_loc(self) -> int:
        return self.ans_loc

class SingleValExpression (Expression):
    def __init__(self, val: int):
        self.val = val

    def translate(self, state: State) -> list[Instruction]:
        # This instruction is necessary if the containing expression is not computable, since MATH instructions require the values to be stored in memory
        self.set_ans_loc(state.claim_mem_addr())
        return [SetInstruction(self.get_ans_loc(), self.get_value())]

    def is_computable(self) -> bool:
        return True

    def get_value(self) -> int:
        return self.val
    
class TreeExpression (Expression):
    def __init__(self, operation: ExpOp, left_exp: Expression, right_exp: Expression):
        self.left_exp: Expression = left_exp
        self.right_exp: Expression = right_exp
        self.operation: ExpOp = operation

    def translate(self, state: State) -> list[Instruction]:
        # First we determine if this expression is computable, because if it is then we just need to store the answer into a memory location
        if self.is_computable():
            value = self.get_value()
            self.set_ans_loc(state.claim_mem_addr())

            return [SetInstruction(self.get_ans_loc(), value)]
        
        # If its not computable, then we need to first convert the two sub expressions to be stored in memory, so we can use the MATH instruction
        
        out_instrs: list[Instruction] = []

        out_instrs.append(self.left_exp.translate())
        out_instrs.append(self.right_exp.translate())

        # At this point, the two input memory locations should be set up, now we need to set up a place to store the answer
        self.set_ans_loc(state.claim_mem_addr())

        # Now we can actually use the math expression
        # TODO: Again, self.operation is using a different operation enum than the MathInstruction, which needs to be resolved
        out_instrs.append(MathInstruction(self.operation, self.left_exp.get_ans_loc(), self.right_exp.get_ans_loc(), self.get_ans_loc()))

        return out_instrs

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