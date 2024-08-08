from compiler import State
from statements import *
from expressions import *
from instructions import *

class Program (Statement):
    def __init__(self, statements: list[Statement] = []):
        self.statements = statements

    def translate(self, state: State) -> list[Instruction]:
        translated_instrs = []
        for statement in self.statements:
            translated_instrs.extend(statement.translate(state))

        translated_instrs.append(StopInstruction())

        # TODO: Need to now compile and append function statements, also need to update placeholder jmps
        for cur_func_data in state.func_dict.values():
            # For each function, we need to translate their body statements,
            # and then append a jmp instruction to return to the caller
            
            for body_instr in cur_func_data.body_statements:
                cur_func_data.start_instr = state.cur_instruction
                translated_instrs.extend(body_instr.translate(state))

            # TODO: Throw a proper error if the return instruction for the function is not deteremined
            if cur_func_data.ret_instr_addr == None:
                return []

            # Add the return jmp
            translated_instrs.append(JmpInstruction(cur_func_data.ret_instr_addr))
            state.cur_instruction += 1

        return translated_instrs
    
    def add_statement(self, statement: Statement) -> None:
        self.statements.append(statement)

if __name__ == '__main__':
    program = Program()

    test_function = FuncDeclStatement('new_func', [
        VarDeclarationStatement('func_var'),
        VarAssignmentStatement('func_var', SingleValExpression(10))
    ],)

    test_declaration = VarDeclarationStatement('test_var')

    test_expression = SingleValExpression(6)
    test_assignment = VarAssignmentStatement('test_var', test_expression)

    second_decl = VarDeclarationStatement('second_var')
    test_move = VarMoveStatement('test_var', 'second_var')

    program.add_statement(test_function)
    program.add_statement(test_declaration)
    program.add_statement(test_assignment)
    program.add_statement(test_assignment)
    program.add_statement(second_decl)
    program.add_statement(test_move)

    def_state = State()
    translated_prog = program.translate(def_state)

    for instr in translated_prog:
        print(instr)