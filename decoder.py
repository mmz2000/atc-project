def stringify_lable(label: int) -> str:
    # A1,B1,C1,D1,E1,A2,B2,C2,D2,E2
    return ["A", "B", "C", "D", "E"][label % 5] + str(label // 5 + 1)


def stringify_symbol(symbol: int) -> str:
    # Y,X1,Z1,...
    if symbol == 0:
        return "Y"
    if symbol % 2 == 0:
        return f"Z{symbol//2}"
    return f"X{symbol//2+1}"


class ProgramLine:
    pass


class ProgramLineAdd(ProgramLine):
    def __init__(self, label: int, symbol: int):
        self.label = label
        self.symbol = symbol

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] {stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} + 1"
        return f"{stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} + 1"


class ProgramLineSub(ProgramLine):
    def __init__(self, label: int, symbol: int):
        self.label = label
        self.symbol = symbol

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] {stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} - 1"
        return f"{stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)} - 1"


class ProgramLineArb(ProgramLine):
    def __init__(self, label: int, symbol: int):
        self.label = label
        self.symbol = symbol

    def __str__(self):
        if self.label > 0:
            return f"[{stringify_lable(self.label-1)}] {stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)}"
        return f"{stringify_symbol(self.symbol)} <- {stringify_symbol(self.symbol)}"


class ProgramLineJumpIf(ProgramLine):
    def __init__(self, label: int, symbol: int, jump_lable: int):
        self.label = label
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


def print_program(*args):
    for i in args:
        label, other = decode(i)
        instruction, symbol = other
        if instruction == 0:
            print(ProgramLineArb(label=label, symbol=symbol))
        elif instruction == 1:
            print(ProgramLineAdd(label=label, symbol=symbol))
        elif instruction == 2:
            print(ProgramLineSub(label=label, symbol=symbol))
        else:
            print(
                ProgramLineJumpIf(
                    label=label, symbol=symbol, jump_lable=instruction - 3
                )
            )


if __name__ == "__main__":
    print_program(*list(map(int, input().split())))
