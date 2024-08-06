class FuncData:
    def __init__(self, body_statements, ret_instr_addr = None, start_instr = None):
        self.body_statements = body_statements
        self.ret_instr_addr = ret_instr_addr
        self.start_instr = start_instr