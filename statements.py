from abc import ABC
from abc import abstractmethod
from state import State
from expression import Expression
from instructions import instrs

class Statement (ABC):
    @abstractmethod
    def translate(self, state: State) -> str:
        pass

class VarDeclarationStatement (Statement):
    def __init__(self, var_name: str):
        self.var_name = var_name

    def translate(self, state: State) -> str:
        state.add_var(self.var_name, state.claim_mem_addr())

        return '' # Return an empty string since this does not translate into an instruction

class VarAssignmentStatement (Statement):
    def __init__(self, var_name: str, exp: Expression):
        self.var_name = var_name
        self.exp = exp

    def translate(self, state: State) -> str:
        var_addr = state.get_var_addr(self.var_name)

        if var_addr == None:
            raise NameError('Unknown variable name')
        
        exp_value = self.exp.get_value() # No need to check for errors because it will raise an exception if invalid

        return f'I: {instrs['set']} 0: {var_addr} 1: {exp_value}\n'
    
