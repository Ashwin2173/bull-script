class ProgramBuilder:
    def __init__(self):
        self.program = list()

    def add(self, other):
        self.program.append(other)

    def __str__(self):
        return ''.join(self.program)
