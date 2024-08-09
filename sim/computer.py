import compiler.instructions as comp_instrs

class Computer:
    def __init__(self, num_mem: int, instrs: list[comp_instrs.Instruction]):
        self.memory_arr: list[None | int] = [None] * num_mem
        self.cur_instr_num: int = 0
        self.instrs: list[comp_instrs.Instruction] = instrs
        self.stopped: bool = False

    def get_mem_val(self, mem_loc: int) -> int:
        #NOTE: mem_loc is 1-indexed
        max_mem_loc = len(self.memory_arr)
        if mem_loc < 1 or mem_loc > max_mem_loc:
            raise IndexError(f'Invalid memory location "{mem_loc}". Must be between 1 and {max_mem_loc}')
        
        found_val = self.memory_arr[mem_loc - 1]
        if found_val == None:
            raise ValueError(f'Attemp to access uninitialized memory address {mem_loc}')
        
        return found_val
    
    def set_mem_val(self, mem_loc: int, new_val: int) -> None:
        #NOTE: mem_loc is 1-indexed
        max_mem_loc = len(self.memory_arr)
        if mem_loc < 1 or mem_loc > max_mem_loc:
            raise IndexError(f'Invalid memory location "{mem_loc}. Must be between 0 and {max_mem_loc}')
        
        self.memory_arr[mem_loc - 1] = new_val

    def reset(self) -> None:
        self.memory_arr = [None for _ in self.memory_arr]
        self.cur_instr_num = 0
        self.stopped = False

    def step(self) -> None:
        if self.stopped:
            raise Exception('Can not step, as the computer has reached a stopped state')

        cur_instr = self.instrs[self.cur_instr_num]

        match cur_instr.name:
            case 'stop':
                self.stopped = True
            case 'set':
                self.set_mem_val(cur_instr.args[0], cur_instr.args[1])
                self.cur_instr_num += 1
            case _:
                self.stopped = True
                raise ValueError(f'Attempt to execute unknown instruction "{cur_instr.name}"')            
                
    def __str__(self) -> str:
        ret_str = '----------\n'
        
        ret_str += f'State: {'Stopped' if self.stopped else 'Running'}\n\n'

        for i in range(len(self.memory_arr)):
            ret_str += f'Addr {i + 1}: {self.memory_arr[i]}\n'

        ret_str += f'\nNext Instr Num: {self.cur_instr_num}\n'

        cur_instr = self.instrs[self.cur_instr_num]
        ret_str += f'Next Instr: ({cur_instr.name}) {cur_instr}\n'
        ret_str += '----------'

        return ret_str

                
if __name__ == '__main__':
    set_instruction = comp_instrs.SetInstruction(1, 10)
    stop_instruction = comp_instrs.StopInstruction()

    computer = Computer(10, [set_instruction, stop_instruction])    

    print(computer)

    computer.step()

    print(computer)

    computer.step()

    print(computer)