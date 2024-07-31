from abc import ABC
from abc import abstractmethod
from state import State
from expressions import Expression
from instructions import instrs

class Statement (ABC):
    @abstractmethod
    def translate(self, state: State) -> str:
        pass



class VarDeclarationStatement (Statement):
    def __init__(self, var_name: str):
        self.var_name = var_name

    def translate(self, state: State) -> str:
        var_addr = state.add_var(self.var_name, state.claim_mem_addr())
        if var_addr == None:
            raise SyntaxError(f'Invalid redeclaration of "{self.var_name}"')

        return '' # Return an empty string since this does not translate into an instruction



class VarAssignmentStatement (Statement):
    def __init__(self, var_name: str, exp: Expression):
        self.var_name = var_name
        self.exp = exp

    def translate(self, state: State) -> str:
        var_addr = state.get_var_addr(self.var_name)

        if var_addr == None:
            raise NameError(f'Unknown variable name "{self.var_name}"')
        
        exp_value = self.exp.get_value(state) # No need to check for errors because it will raise an exception if invalid

        return f'I: {instrs["set"]} 0: {var_addr} 1: {exp_value}\n'



class VarMoveStatement (Statement):
    def __init__(self, from_var_name: str, to_var_name: str):
        self.from_var_name = from_var_name
        self.to_var_name = to_var_name

    def translate(self, state: State) -> str:
        from_addr = state.get_var_addr(self.from_var_name)

        if from_addr == None:
            raise NameError(f'Unknown variable name "{self.from_var_name}"')
        
        to_addr = state.get_var_addr(self.to_var_name)

        if to_addr == None:
            raise NameError(f'Unknown variable name "{self.to_var_name}')
        
        return f'I: {instrs["mov"]} 0: {from_addr} 1: {to_addr}\n'