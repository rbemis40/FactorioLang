from compiler.core import Instruction
from compiler.instructions import MathInstruction, JmpIfInstruction

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from computer import Computer

def handle_instr(comp: 'Computer', instr: Instruction) -> None:
     match instr.name:
            case 'stop':
                handle_stop(comp)
            case 'set':
                handle_set(comp, instr)
            case 'jmp':
                handle_jmp(comp, instr)
            case 'math':
                handle_math(comp, instr)
            case 'mov':
                handle_mov(comp, instr)
            case 'jif':
                handle_jif(comp, instr)
            case _:
                comp.stopped = True
                raise ValueError(f'Attempt to execute unknown instruction "{instr.name}"')

def handle_stop(comp: 'Computer') -> None:
    comp.stopped = True

def handle_set(comp: 'Computer', instr: Instruction) -> None:
    comp.set_mem_val(instr.args[0], instr.args[1])
    comp.inc_instr_counter()

def handle_jmp(comp: 'Computer', instr: Instruction) -> None:
    jmp_loc = comp.get_mem_val(instr.args[0])
    comp.set_instr_counter(jmp_loc)

def handle_math(comp: 'Computer', instr: Instruction) -> None:
    operation = instr.args[0]
    left_val = comp.get_mem_val(instr.args[1])
    right_val = comp.get_mem_val(instr.args[2])

    result = None

    match operation:
        case MathInstruction.ADD:
            result = left_val + right_val
        case MathInstruction.SUB:
            result = left_val - right_val
        case MathInstruction.MUL:
            result = left_val * right_val
        case MathInstruction.DIV:
            result = left_val // right_val
        case MathInstruction.MOD:
            result = left_val % right_val
        case _:
            raise ValueError(f'Invalid math operation {operation}')
        
    store_addr = instr.args[3]
    comp.set_mem_val(store_addr, result)

    comp.inc_instr_counter()

def handle_mov(comp: 'Computer', instr: Instruction) -> None:
    val = comp.get_mem_val(instr.args[0])
    comp.set_mem_val(instr.args[1], val)
    comp.inc_instr_counter()

def handle_jif(comp: 'Computer', instr: Instruction) -> None:
    left_val = comp.get_mem_val(instr.args[0])
    right_val = comp.get_mem_val(instr.args[1])

    operation = instr.args[2]

    result = None
    match operation:
        case JmpIfInstruction.GT:
            result = left_val > right_val
        case JmpIfInstruction.LT:
            result = left_val < right_val
        case JmpIfInstruction.EQ:
            result = left_val == right_val

    if result:
        jmp_loc = comp.get_mem_val(instr.args[3])
        comp.set_instr_counter(jmp_loc)
    else:
        comp.inc_instr_counter()