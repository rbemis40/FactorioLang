from compiler.core import State, Translatable
from compiler.statements import *
from compiler.expressions import *
from compiler.instructions import *

class Program (Translatable):
    def __init__(self, statements: list[Translatable] = []):
        self.statements: list[Translatable] = statements

    def translate(self, state: State) -> list[Instruction]:
        translated_instrs: list[Instruction] = []
        for statement in self.statements:
            translated_instrs.extend(statement.translate(state))

        translated_instrs.append(StopInstruction())

        # TODO: Need to now compile and append function statements, also need to update placeholder jmps
        for cur_func_data in state.func_dict.values():
            # For each function, we need to translate their body statements,
            # and then append a jmp instruction to return to the caller
            
            cur_func_data.start_instr = state.cur_instruction # Notes where in memory the first instruction of the funciton will be
            for body_instr in cur_func_data.body_statements:
                translated_instrs.extend(body_instr.translate(state))

            if cur_func_data.ret_instr_addr == None:
                raise Exception(f'Unable to translate function "{cur_func_data.name}", unknown return address')

            # Add the return jmp to the caller (the instruction # to jump to is stored in memory location ret_instr_addr)
            translated_instrs.append(JmpInstruction(cur_func_data.ret_instr_addr))
            state.cur_instruction += 1

        return translated_instrs
    
    def add_statement(self, statement: Translatable) -> None:
        self.statements.append(statement)

if __name__ == '__main__':
    test_expr = TreeExpression(ExpOp.ADD,
        TreeExpression(ExpOp.MUL,
            SingleValExpression(9),
            SingleValExpression(10)               
        ),                           
        TreeExpression(ExpOp.MUL,
            SingleValExpression(4),
            VarExpression('expr_var')
        )                     
    )

    statements: list[Translatable] = [
        VarDeclarationStatement('test_var'),
        VarDeclarationStatement('expr_var'),
        ExprAssignmentStatement('expr_var', SingleValExpression(13)),
        ExprAssignmentStatement('test_var', test_expr)
    ]

    def_state = State()

    program = Program(statements)
    translated_prog = program.translate(def_state)

    for instr in translated_prog:
        print(instr)