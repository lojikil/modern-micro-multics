#@(#) a very simple-forth/joy/cat-alike for compiling to MMM Assembly
#@(#) named after the character from A Mid-Summer Night's Dream; I was
#@(#) originally thinking about implementing Oberon, but looking for
#@(#) a smaller one...
#@(#) also makes me really appreciative of the tools I get for free
#@(#) in Reason/SML/OCaml/Haskell

class PuckAST:
    def compile(self):
        raise NotImplemented()
    pass

class PuckInt(PuckAST):
    def __init__(self, i):
        self.i = i

    def depth(self):
        return 1

    def __str__(self):
        return "ldi {0}".format(self.i)

class PuckFloat(PuckAST):
    def __init__(self, f):
        self.f = f

    def depth(self):
        return 1

    def __str__(self):
        return "ldr {0}".format(self.f)

class PuckBool(PuckAST):
    def __init__(self, b):
        self.b = b

    def depth(self):
        return 1

    def __str__(self):
        return "ldb {0}".format(self.b)

class PuckString(PuckAST):
    def __init__(self, s):
        self.s = s

    def depth(self):
        return 1

    def __str__(self):
        return "lds {0}".format(self.s)

class PuckIf(PuckAST):
    def __init__(self, cond, then, el):
        self.cond = cond
        self.then = then
        self.el = el

    def depth(self):
        return self.cond.depth() + self.then.depth() + self.el.depth()

    def __str__(self, offset=0):
        cond = str(self.cond)
        ocond = self.cond.depth()
        dthen = self.then.depth()
        then = str(self.then)
        el = str(self.el)
        othen = ocond + 2
        oelse = ocond + 3 + dthen
        # NOTE: we have to put a NOP & a jump over the
        # else form, so that we don't accidentally run
        # that each time too...
        res = "{0}\njpc {1}\njmp {2}\n{3}\njmp {5}\n{4}\nnop\n"
        return res.format(cond, othen, oelse, then, el, oelse + 1)

class PuckBlock(PuckAST):
    def __init__(self, block):
        self.block = block

    def depth(self):
        # would be so much nicer with a fold_*
        res = 0
        for b in self.block:
            res += b.depth()
        return res

    def __str__(self, offset=0):
        return "\n".join([str(x) for x in self.block])

class PuckOp(PuckAST):
    def __init__(self, op):
        self.op = op
        self.oplist = [ "+", "-", "*", "/", "%", "<<", ">>", "&", "|", "^",
                        "~", "neg", "not", "<", "<=", ">", ">=", "==", "!="]

    def depth(self):
        return 1

    def __str__(self):
        return "opr {0}".format(self.oplist.index(self.op))

class Puck:
    def __init__(self):
        self.current_line = 0
        self.current_word = ""

    def next_lexeme(self, src, offset):
        pass

    def parse(self, src) -> PuckAST:
        pass
        #(nextl, o) = self.next_lexeme(src, 0)
        #while nextl != T:
        #    pass
