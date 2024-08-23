import compiler.instructions as comp_instrs
from time import sleep
from sim.instr_behaviors import handle_instr

class Computer:
    def __init__(self, num_mem: int, instrs: list[comp_instrs.Instruction]):
        self.memory_arr: list[None | int] = [None] * num_mem
        self.cur_instr_num: int = 1 # Instructions are 1-indexed
        self.instrs: list[comp_instrs.Instruction] = instrs
        self.stopped: bool = False

    def get_mem_val(self, mem_loc: int) -> int:
        #NOTE: mem_loc is 1-indexed
        max_mem_loc = len(self.memory_arr)
        if mem_loc < 1 or mem_loc > max_mem_loc:
            raise IndexError(f'Invalid memory location "{mem_loc}". Must be between 1 and {max_mem_loc}')
        
        found_val = self.memory_arr[mem_loc - 1]
        if found_val == None:
            raise ValueError(f'Attempt to access uninitialized memory address {mem_loc}')
        
        return found_val
    
    def set_mem_val(self, mem_loc: int, new_val: int) -> None:
        #NOTE: mem_loc is 1-indexed
        max_mem_loc = len(self.memory_arr)
        if mem_loc < 1 or mem_loc > max_mem_loc:
            raise IndexError(f'Invalid memory location "{mem_loc}. Must be between 0 and {max_mem_loc}')
        
        self.memory_arr[mem_loc - 1] = new_val

    def inc_instr_counter(self) -> None:
        if self.cur_instr_num + 1 > len(self.instrs):
            raise ValueError(f'Can not increment instruction counter to {self.cur_instr_num + 1}, only {len(self.instrs)} instructions')

        self.cur_instr_num += 1 

    def set_instr_counter(self, new_num: int) -> None:
        if new_num < 1 or new_num >= len(self.instrs):
            raise ValueError(f'Invalid attempt to set instruction counter to {new_num}, must be between 1 and {len(self.instrs)}')

        self.cur_instr_num = new_num

    def get_cur_instr(self) -> comp_instrs.Instruction:
        if self.cur_instr_num < 1 or self.cur_instr_num > len(self.instrs):
            raise ValueError(f'Invalid attempt to get instruction {self.cur_instr_num}, must be between 1 and {len(self.instrs)}')

        # NOTE: Minus 1 because the instruction counter is 1-indexed
        return self.instrs[self.cur_instr_num - 1]

    def reset(self) -> None:
        self.memory_arr = [None for _ in self.memory_arr]
        self.cur_instr_num = 1
        self.stopped = False

    def step(self) -> None:
        if self.stopped:
            raise Exception('Can not step, as the computer has reached a stopped state')

        cur_instr = self.get_cur_instr()

        handle_instr(self, cur_instr)            
                
    def __str__(self) -> str:
        ret_str = '----------\n'
        
        ret_str += f'State: {"Stopped" if self.stopped else "Running"}\n\n'

        for i in range(len(self.memory_arr)):
            ret_str += f'Addr {i + 1}: {self.memory_arr[i]}\n'

        ret_str += f'\nNext Instr Num: {self.cur_instr_num}\n'

        cur_instr = self.get_cur_instr()
        ret_str += f'Next Instr: ({cur_instr.name}) {cur_instr}\n'
        ret_str += '----------'

        return ret_str

                
if __name__ == '__main__':
    #I: 2 0: 2 1: 13
    #I: 2 0: 3 1: 90
    #I: 2 0: 4 1: 4
    #I: 4 0: 3 1: 4 2: 2 3: 4
    #I: 4 0: 1 1: 3 2: 4 3: 3
    #I: 5 0: 3 1: 1
    #I: 1

    instrs = [
        comp_instrs.SetInstruction(2, 13),
        comp_instrs.SetInstruction(3, 90),
        comp_instrs.SetInstruction(4, 4),
        comp_instrs.MathInstruction(3, 4, 2, 4),
        comp_instrs.MathInstruction(1, 3, 4, 3),
        comp_instrs.MovInstruction(3, 1),
        comp_instrs.StopInstruction()
    ]

    computer = Computer(10, instrs)    

    while not computer.stopped:
        print(computer)
        computer.step()
        sleep(0.5)

    print(computer)