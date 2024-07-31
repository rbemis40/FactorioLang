from state import State

class Expression:
    def get_value(self, state: State) -> int:
        pass

class SingleValExpression (Expression):
    def __init__(self, val: int):
        self.val = val

    def get_value(self, state: State) -> int:
        return self.val