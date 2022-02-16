# @(#) a very simple VM, reminiscent of both SECD and P-Code machine
# @(#) keep things light and simple honestly

class VM(object):
    def __init__(self):
        self.stack = []
        self.env = {}
        self.control = 0
        self.dump = []
        self.vmhalt = False
        self.csp = {}

    def run(self, program):
        lines = program.split('\n')
        prg = []
        for line in lines:
            prg.append(self.decode_instruction(line))

        while not self.vmhalt and self.control < len(prg):
            (op, operand) = prg[self.control]
            self.execute(op, operand)
            if op != "jmp" and op != "jpc":
                self.control = self.control + 1

    def add_csp(self, syscall, f, arity):
        self.csp[syscall] = [f, arity]

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
            iopr = int(operand)
            if iopr == 0:
                # print
                opr0 = self.stack.pop()
                print(opr0)
            elif iopr == 1:
                # readline
                opr0 = self.stack.pop()
                stack.append(input(opr0))
            elif iopr == 2:
                # string_of
                opr0 = self.stack.pop()
                stack.append(str(opr0))
            elif iopr == 3:
                # int_of_string
                opr0 = self.stack.pop()
                stack.append(int(opr0))
            elif iopr == 4:
                # hex_of_string
                opr0 = self.stack.pop()
                stack.append(int(opr0, base=16))
            elif iopr == 5:
                # oct_of_string
                opr0 = self.stack.pop()
                stack.append(int(opr0, base=8))
            elif iopr == 6:
                # bin_of_string
                opr0 = self.stack.pop()
                stack.append(int(opr0, base=2))
            elif iopr == 7:
                # float_of_string
                opr0 = self.stack.pop()
                stack.append(float(opr0))
            pass
        elif op == "cup":
            # call user procedure
            pass
        elif op == "opr":
            iopr = int(operand)
            # arithemetic operators
            if iopr == 0:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 + opr1)
            elif iopr == 1:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 - opr1)
            elif iopr == 2:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 * opr1)
            elif iopr == 3:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 / opr1)
            elif iopr == 4:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 % opr1)
            # bitwise
            elif iopr == 5:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 << opr1)
            elif iopr == 6:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 >> opr1)
            elif iopr == 7:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 & opr1)
            elif iopr == 8:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 | opr1)
            elif iopr == 9:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 ^ opr1)
            # logical, arithmetic, and bitwise negation
            elif iopr == 10:
                opr0 = self.stack.pop()
                self.stack.append(~opr0)
            elif iopr == 11:
                opr0 = self.stack.pop()
                self.stack.append(-opr0)
            elif iopr == 12:
                opr0 = self.stack.pop()
                self.stack.append(not opr0)
            # logical comparison operators
            elif iopr == 13:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 < opr1)
            elif iopr == 14:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 <= opr1)
            elif iopr == 15:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 > opr1)
            elif iopr == 16:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 >= opr1)
            elif iopr == 17:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 == opr1)
            elif iopr == 18:
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0 != opr1)
            # stack operations
            elif iopr == 19:
                # dup
                self.stack.append(self.stack[-1])
            elif iopr == 20:
                # drop
                self.stack.pop()
            elif iopr == 21:
                # swap
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr0)
                self.stack.append(opr1)
            elif iopr == 22:
                # over
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                self.stack.append(opr1)
                self.stack.append(opr0)
                self.stack.append(opr1)
            elif iopr == 23:
                # rot
                opr0 = self.stack.pop()
                opr1 = self.stack.pop()
                opr2 = self.stack.pop()
                self.stack.append(opr1)
                self.stack.append(opr0)
                self.stack.append(opr2)
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

