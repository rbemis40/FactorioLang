from compiler.core import Instruction

# This is a temporary instruction that represents a placeholder until the jmp location into a function can be determined at the end of compilation
class FuncPlaceholderInstruction (Instruction):
    def __init__(self, func_name: str):
        super().__init__('func_placeholder', -1, [])
        self.func_name: str = func_name

class StopInstruction (Instruction):
    def __init__(self):
        super().__init__('stop', 1, [])

class SetInstruction (Instruction):
    def __init__(self, var_addr: int, value: int):
        super().__init__('set', 2, [var_addr, value])


class JmpInstruction (Instruction):
    def __init__(self, instr_mem_addr: int):
        super().__init__('jmp', 3, [instr_mem_addr])


class MathInstruction (Instruction):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    MOD = 5

    def __init__(self, operation: int, left_addr: int, right_addr: int, store_addr: int):
        super().__init__('math', 4, [operation, left_addr, right_addr, store_addr])


class MovInstruction (Instruction):
    def __init__(self, from_addr: int, to_addr: int):
        super().__init__('mov', 5, [from_addr, to_addr])