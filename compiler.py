from typing import Optional
from abc import ABC, abstractmethod

# class State
#   - Holds the current information needed to translate statements into machine instructions
#   - Variables:
#       - var_dict: A dictionary [variable name] --> [memory location]
#       - func_dict: A dictionary [function name] --> [instruction number]
#       - cur_mem_addr: Stores the next memory address that is available for use (such as declaring variables)
#       - cur_instruction: Stores the current instruction number, for use such as jumping to functions


class State:
    def __init__(self, def_vars: dict[str, int] = {}, def_funcs: dict[str, 'FuncData'] = {}):
        self.var_dict = def_vars
        self.func_dict = def_funcs

        self.cur_mem_addr = 1

        self.cur_instruction = 1

    def get_var_addr(self, var_name: str) -> Optional[int]:
        if var_name not in self.var_dict:
            return None

        return self.var_dict[var_name]
    
    def add_var(self, var_name: str, addr: int) -> Optional[int]:
        if var_name in self.var_dict:
            return None

        self.var_dict[var_name] = addr

        return addr
    
    def get_func_data(self, func_name: str) -> Optional['FuncData']:
        if func_name not in self.func_dict:
            return None
        
        return self.func_dict[func_name]
    
    def add_func(self, func_name: str , func_data: 'FuncData') -> Optional['FuncData']:
        if func_name in self.func_dict:
            return None
        
        self.func_dict[func_name] = func_data

        return func_data
    
    def claim_mem_addr(self):
        claimed_addr = self.cur_mem_addr
        self.cur_mem_addr += 1

        return claimed_addr
    
class Instruction:
    def __init__(self, name: str, id: int, args: list[int]):
        self.name = name
        self.id = id
        self.args = args

    def __str__(self) -> str:
        ret_str = f'I: {self.id}'
        for i, arg in enumerate(self.args):
            ret_str += f' {i}: {arg}'

        return ret_str


class Statement (ABC):
    @abstractmethod
    def translate(self, state) -> list[Instruction]:
        pass

class FuncData:
    def __init__(self, body_statements: list[Statement], ret_instr_addr: Optional[int] = None, start_instr: Optional[int] = None):
        self.body_statements = body_statements
        self.ret_instr_addr = ret_instr_addr
        self.start_instr = start_instr