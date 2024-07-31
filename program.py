from state import State
from statement import Statement

class Program (Statement):
    def __init__(self, statements: list[Statement] = []):
        self.statements = statements

    def translate(self, state: State) -> str:
        pass

if __name__ == '__main__':
    program = Program()