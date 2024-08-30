from compiler.core import State, Translatable, Instruction
from compiler.instructions import SetInstruction, MathInstruction
from enum import Enum
from abc import abstractmethod

# TODO: Avoid redefining this in statements.py
class ExpOp (Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    MOD = 5

class Expression (Translatable):
    def __init__(self):
        self.ans_loc: int = 0 # This will be used to store the memory location of the expressions answer for use in other expressions, 0 for placeholder
    
    @abstractmethod
    def is_computable(self) -> bool:
        pass

    @abstractmethod
    def get_value(self) -> int:
        pass

    def unclaim_mem(self, state: State) -> None:
        return

    def set_ans_loc(self, new_loc: int) -> None:
        self.ans_loc = new_loc

    def get_ans_loc(self) -> int:
        return self.ans_loc

class SingleValExpression (Expression):
    def __init__(self, val: int):
        self.val: int = val

    def translate(self, state: State) -> list[Instruction]:
        # This instruction is necessary if the containing expression is not computable, since MATH instructions require the values to be stored in memory
        self.set_ans_loc(state.claim_mem_addr())
        return [SetInstruction(self.get_ans_loc(), self.get_value())]

    def is_computable(self) -> bool:
        return True

    def get_value(self) -> int:
        return self.val
    
    def unclaim_mem(self, state: State) -> None:
        state.unclaim_mem_addr(self.get_ans_loc())


 
# Note: We can't implement unclaim_mem because the variable may be used elsewhere after the expression
class VarExpression (Expression):
    def __init__(self, var_name: str):
        self.var_name: str = var_name

    def translate(self, state: State) -> list[Instruction]:
        # Because we already have the stored location (the variable's address), we just have to make sure the variable exists

        var_addr: (int | None) = state.get_var_addr(self.var_name)
        if var_addr == None:
            raise NameError(f'Unknown variable name "{self.var_name}"')


        # There will be no instructions necessary, since the variable already has a place in memory
        self.set_ans_loc(var_addr)

        return []

    def is_computable(self) -> bool:
        return False
    
    def get_value(self) -> int:
        raise ValueError('Attempted to get value of non-computable expression')
    

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

        out_instrs.extend(self.left_exp.translate(state))
        out_instrs.extend(self.right_exp.translate(state))

        # We can free the sub expression memory addresses, since they have already been computed at this point
        self.left_exp.unclaim_mem(state)
        self.right_exp.unclaim_mem(state)

        # At this point, the two input memory locations should be set up, now we need to set up a place to store the answer
        self.set_ans_loc(state.claim_mem_addr())

        # Now we can actually use the math expression
        # TODO: Again, self.operation is using a different operation enum than the MathInstruction, which needs to be resolved
        out_instrs.append(MathInstruction(self.operation.value, self.left_exp.get_ans_loc(), self.right_exp.get_ans_loc(), self.get_ans_loc()))

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
            
    def unclaim_mem(self, state: State) -> None:
        state.unclaim_mem_addr(self.get_ans_loc())