import compiler.instructions as comp_instrs
from time import sleep

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

        match cur_instr.name:
            case 'stop':
                self.stopped = True
            case 'set':
                self.set_mem_val(cur_instr.args[0], cur_instr.args[1])
                self.inc_instr_counter()
            case 'jmp':
                jmp_loc = self.get_mem_val(cur_instr.args[0])
                self.set_instr_counter(jmp_loc)
            case 'math':
                operation = cur_instr.args[0]
                left_val = self.get_mem_val(cur_instr.args[1])
                right_val = self.get_mem_val(cur_instr.args[2])

                result = None

                match operation:
                    case comp_instrs.MathInstruction.ADD:
                        result = left_val + right_val
                    case comp_instrs.MathInstruction.SUB:
                        result = left_val - right_val
                    case comp_instrs.MathInstruction.MUL:
                        result = left_val * right_val
                    case comp_instrs.MathInstruction.DIV:
                        result = left_val // right_val
                    case comp_instrs.MathInstruction.MOD:
                        result = left_val % right_val
                    case _:
                        raise ValueError(f'Invalid math operation {operation}')
                    
                store_addr = cur_instr.args[3]
                self.set_mem_val(store_addr, result)

                self.inc_instr_counter()
            case 'mov':
                val = self.get_mem_val(cur_instr.args[0])
                self.set_mem_val(cur_instr.args[1], val)
                self.inc_instr_counter()
            case 'jif':
                left_val = self.get_mem_val(cur_instr.args[0])
                right_val = self.get_mem_val(cur_instr.args[1])

                operation = cur_instr.args[2]

                result = None
                match operation:
                    case comp_instrs.JmpIfInstruction.GT:
                        result = left_val > right_val
                    case comp_instrs.JmpIfInstruction.LT:
                        result = left_val < right_val
                    case comp_instrs.JmpIfInstruction.EQ:
                        result = left_val == right_val

                if result:
                    jmp_loc = self.get_mem_val(cur_instr.args[3])
                    self.set_instr_counter(jmp_loc)
                else:
                    self.inc_instr_counter()
            case _:
                self.stopped = True
                raise ValueError(f'Attempt to execute unknown instruction "{cur_instr.name}"')            
                
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
    instrs = [
        comp_instrs.SetInstruction(1, 4), # Where to jmp to
        comp_instrs.SetInstruction(2, 1), # What to add by
        comp_instrs.SetInstruction(3, 0), # Current iteration
        comp_instrs.SetInstruction(4, 7), # When to stop
        comp_instrs.MathInstruction(comp_instrs.MathInstruction.ADD, 2, 3, 3),
        comp_instrs.JmpIfInstruction(3, 4, comp_instrs.JmpIfInstruction.LT, 1),
        comp_instrs.StopInstruction()
    ]

    computer = Computer(10, instrs)    

    while not computer.stopped:
        print(computer)
        computer.step()
        sleep(0.5)

    print(computer)