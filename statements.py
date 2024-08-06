from abc import ABC, abstractmethod
from state import State
from expressions import Expression
from instructions import *
from functions import FuncData

class Statement (ABC):
    @abstractmethod
    def translate(self, state: State) -> list[Instruction]:
        pass



class VarDeclarationStatement (Statement):
    def __init__(self, var_name: str):
        self.var_name = var_name

    def translate(self, state: State) -> list[Instruction]:
        var_addr = state.add_var(self.var_name, state.claim_mem_addr())
        if var_addr == None:
            raise SyntaxError(f'Invalid redeclaration of "{self.var_name}"')

        return [] # Return an list since it does not result in an instruction



class VarAssignmentStatement (Statement):
    def __init__(self, var_name: str, exp: Expression):
        self.var_name = var_name
        self.exp = exp

    def translate(self, state: State) -> list[Instruction]:
        var_addr = state.get_var_addr(self.var_name)

        if var_addr == None:
            raise NameError(f'Unknown variable name "{self.var_name}"')
        
        exp_value = self.exp.get_value(state) # No need to check for errors because it will raise an exception if invalid

        state.cur_instruction += 1

        return [SetInstruction(var_addr, exp_value)]


class VarMoveStatement (Statement):
    def __init__(self, from_var_name: str, to_var_name: str):
        self.from_var_name = from_var_name
        self.to_var_name = to_var_name

    def translate(self, state: State) -> list[Instruction]:
        from_addr = state.get_var_addr(self.from_var_name)

        if from_addr == None:
            raise NameError(f'Unknown variable name "{self.from_var_name}"')
        
        to_addr = state.get_var_addr(self.to_var_name)

        if to_addr == None:
            raise NameError(f'Unknown variable name "{self.to_var_name}')
        
        state.cur_instruction += 1

        return [MovInstruction(from_addr, to_addr)]    


class FuncDeclStatement (Statement):
    def __init__(self, func_name: str, statements: list[Statement]):
        self.func_name = func_name
        # For now, we create a place holder func_data, because we only figure out the information during translation
        self.func_data = FuncData(statements)

    def translate(self, state: State) -> list[Instruction]:
        # For now, we just update the state to note that the function is now declared
        # When it is time to actually translate it, we will use translate_body
        state.add_func(self.func_name, self.func_data)

        # We will also reserve a place in memory to store the return instruction
        self.func_data.ret_instr_addr = state.claim_mem_addr()

        # We still don't know where in the program the first instruction of the function is going to be placed, so we can't update
        # that piece of func_data yet (will be done in translate_body)

        return []

    def translate_body(self, state: State) -> list[Instruction]:
        # Now we finally know where this function is being stored in memory, so:
        self.func_data.start_instr = state.cur_instruction
        
        func_body_statements = []
        for statement in self.statements:
            func_body_statements.extend(statement.translate(state))

        
        # We also need to add one instruction to jump back to the return address (stored in func_data)

        func_body_statements.append(JmpInstruction(self.func_data.ret_instr_addr))
        state.cur_instruction += 1

        return func_body_statements
        