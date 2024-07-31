from state import State
from statements import *
from expressions import *

class Program (Statement):
    def __init__(self, statements: list[Statement] = []):
        self.statements = statements

    def translate(self, state: State) -> str:
        translated_str = ''
        for statement in self.statements:
            translated_str += statement.translate(state)

        return translated_str
    
    def add_statement(self, statement: Statement) -> None:
        self.statements.append(statement)

if __name__ == '__main__':
    program = Program()

    test_declaration = VarDeclarationStatement('test_var')

    test_expression = SingleValExpression(6)
    test_assignment = VarAssignmentStatement('test_var', test_expression)

    second_decl = VarDeclarationStatement('second_var')
    test_move = VarMoveStatement('test_var', 'second_var')

    program.add_statement(test_declaration)
    program.add_statement(test_assignment)
    program.add_statement(test_assignment)
    program.add_statement(second_decl)
    program.add_statement(test_move)

    def_state = State()
    translated_prog = program.translate(def_state)

    print(translated_prog)