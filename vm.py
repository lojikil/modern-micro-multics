# @(#) a very simple VM, reminiscent of both SECD and P-Code machine
# @(#) keep things light and simple honestly

class VM(object):
    def __init__(self):
        self.stack = []
        self.env = {}
        self.control = 0
        self.dump = []
        self.vmhalt = False

    def run(self, program):
        lines = program.split('\n')
        prg = []
        for line in lines:
            prg.append(self.decode_instruction(line))

        while not self.vmhalt and self.control < len(prg):
            print(prg[self.control])
            (op, operand) = prg[self.control]
            self.execute(op, operand)
            if op != "jmp" and op != "jpc":
                self.control = self.control + 1

    def decode_instruction(self, src):
        # eventually I'd like to do something better here
        # but for now this is fine...
        return tuple(src.split(' ', maxsplit=1))

    def execute(self, op, operand):
        # this alone would make me switch to python3.10
        # very simple combination of SECD style & P-machine
        # instructions. We have some basic load & store
        # instructions, and most things operate on the stack
        if op == "ldi":
            self.stack.append(int(operand))
        elif op == "ldr":
            self.stack.append(float(operand))
        elif op == "lds":
            self.stack.append(operand)
        elif op == "ldb":
            self.stack.append(bool(operand))
        elif op == "lod":
            self.stack.append(self.env[operand])
        elif op == "sto":
            self.env[operand] = self.stack.pop()
        elif op == "csp":
            # call system procedure
            pass
        elif op == "cup":
            # call user procedure
            pass
        elif op == "opr":
            pass
        elif op == "ret":
            pass
        elif op == "jmp":
            self.control = int(operand)
        elif op == "jpc":
            cnd = self.stack.pop()
            if cnd:
                self.control = int(operand)
            else:
                self.control += 1

