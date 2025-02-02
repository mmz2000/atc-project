from collections import defaultdict


class ProgramLine:
    pass


class ProgramLineAdd(ProgramLine):
    def __init__(self, label: int, symbol: int):
        self.label = label - 1
        self.symbol = symbol

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] {stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} + 1"
        return f"{stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} + 1"


class ProgramLineSub(ProgramLine):
    def __init__(self, label: int, symbol: int):
        self.label = label - 1
        self.symbol = symbol

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] {stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} - 1"
        return f"{stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} - 1"


class ProgramLineArb(ProgramLine):
    def __init__(self, label: int, symbol: int):
        self.label = label - 1
        self.symbol = symbol

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] {stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)}"
        return f"{stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)}"


class ProgramLineJumpIf(ProgramLine):
    def __init__(self, label: int, symbol: int, jump_lable: int):
        self.label = label - 1
        self.symbol = symbol
        self.jump_lable = jump_lable

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] IF {stringify_symbol(self.symbol)} != 0 GOTO {stringify_lable(self.jump_lable)}"
        return f"IF {stringify_symbol(self.symbol)} != 0 GOTO {stringify_lable(self.jump_lable)}"


def decode1(code: int) -> (int, int):
    r = 1
    x = 0
    while (code + 1) % (r * 2) == 0:
        r *= 2
        x += 1
    y = (((code + 1) // r) - 1) // 2
    return (x, y)


def decode(code: int) -> (int, (int, int)):
    (x, y) = decode1(code=code)
    return (x, decode1(y))


class Program:
    def __init__(self, *args):
        self.program_lines = [self.decode(arg) for arg in args]
        self.labels = defaultdict(lambda: len(self.program_lines))
        self.prepare_labels()
        self.prepare_arb_vars()
        self.prepare_inputs()

    def decode(self, args):
        label, other = decode(args)
        instruction, symbol = other
        if instruction == 0:
            return ProgramLineArb(label=label, symbol=symbol)
        elif instruction == 1:
            return ProgramLineAdd(label=label, symbol=symbol)
        elif instruction == 2:
            return ProgramLineSub(label=label, symbol=symbol)
        else:
            return ProgramLineJumpIf(
                label=label, symbol=symbol, jump_lable=instruction - 3
            )

    def prepare_labels(self):
        for i in range(len(self.program_lines)):
            if self.program_lines[i].label < 0:
                continue
            if self.labels[self.program_lines[i].label] != len(
                self.program_lines
            ):
                continue
            self.labels[self.program_lines[i].label] = i

    def prepare_arb_vars(self):
        max_ = 0
        for i in self.program_lines:
            if i.symbol == 0:
                continue
            if i.symbol % 2 == 1:
                continue
            if i.symbol // 2 > max_:
                max_ = i.symbol // 2
        self.arb_vars = [0 for _ in range(max_)]

    def prepare_inputs(self):
        max_ = 0
        for i in self.program_lines:
            if i.symbol == 0:
                continue
            if i.symbol % 2 == 0:
                continue
            if (i.symbol // 2) + 1 > max_:
                max_ = (i.symbol // 2) + 1
        self.inputs = [0 for _ in range(max_)]

    def run(self, *inputs):
        for i in range(len(inputs)):
            if i < len(self.inputs):
                self.inputs[i] = inputs[i]
            else:
                self.inputs.append(inputs[i])
        line = 0
        out = 0
        while line < len(self.program_lines):
            print(
                line + 1,
                " ".join([str(i) for i in self.inputs]),
                " ".join([str(i) for i in self.arb_vars]),
                out,
            )
            program_line = self.program_lines[line]
            if isinstance(program_line, ProgramLineAdd):
                if program_line.symbol == 0:
                    out += 1
                elif program_line.symbol % 2 == 0:
                    self.arb_vars[(program_line.symbol // 2) - 1] += 1
                else:
                    self.inputs[program_line.symbol // 2] += 1
                line += 1
            elif isinstance(program_line, ProgramLineSub):
                if program_line.symbol == 0:
                    out -= 1
                elif program_line.symbol % 2 == 0:
                    self.arb_vars[(program_line.symbol // 2) - 1] -= 1
                else:
                    self.inputs[program_line.symbol // 2] -= 1
                line += 1
            elif isinstance(program_line, ProgramLineArb):
                line += 1
            elif isinstance(program_line, ProgramLineJumpIf):
                if program_line.symbol == 0:
                    val = out
                elif program_line.symbol % 2 == 0:
                    val = self.arb_vars[(program_line.symbol // 2) - 1]
                else:
                    val = self.inputs[program_line.symbol // 2]
                if val != 0:
                    line = self.labels[program_line.jump_lable]
                else:
                    line += 1


if __name__ == "__main__":
    program = Program(*list(map(int, input().split())))
    program.run(*list(map(int, input().split())))
