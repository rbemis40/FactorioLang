import compiler.instructions as comp_instrs

class Computer:
    def __init__(self, num_mem: int):
        self.memory_arr: list[None | int] = [None] * num_mem

    def get_mem_val(self, mem_loc: int) -> int:
        max_mem_loc = len(self.memory_arr) - 1
        if mem_loc < 0 or mem_loc > max_mem_loc:
            raise IndexError(f'Invalid memory location "{mem_loc}". Must be between 0 and {max_mem_loc}')
        
        found_val = self.memory_arr[mem_loc]
        if found_val == None:
            raise ValueError(f'Attemp to access uninitialized memory address {mem_loc}')
        
        return found_val
    
    def set_mem_val(self, mem_loc: int, new_val: int) -> None:
        max_mem_loc = len(self.memory_arr) - 1
        if mem_loc < 0 or mem_loc > max_mem_loc:
            raise IndexError(f'Invalid memory location "{mem_loc}. Must be between 0 and {max_mem_loc}')
        
        self.memory_arr[mem_loc] = new_val

    def reset_mem(self):
        self.memory_arr = [None for _ in self.memory_arr]

    def execute_instructions(self, instrs: list[comp_instrs.Instruction]):
        for cur_instr in instrs:
            match cur_instr.name:
                case 'set':
                    print('Set instruction')
                case _:
                    raise ValueError(f'Attempt to execute unknown instruction "{cur_instr.name}"')