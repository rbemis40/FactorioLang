from state import State
from statements import Statement

class Program (Statement):
    def __init__(self, statements: list[Statement] = []):
        self.statements = statements

    def translate(self, state: State) -> str:
        translated_str = ''
        for statement in self.statements:
            translated_str += statement.translate()

        return translated_str

if __name__ == '__main__':
    program = Program()
    translated_prog = program.translate()

    print(translated_prog)