from abc import ABC
from abc import abstractmethod
from state import State

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

