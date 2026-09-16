def unbleach(n: str) -> str:
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')


class WhitespaceError(Exception):
    pass


class _WhitespaceVM:
    SPACE = " "
    TAB = "\t"
    LF = "\n"

    # Instruction groups (IMPs)
    IMP_STACK = SPACE
    IMP_ARITH = TAB + SPACE
    IMP_HEAP  = TAB + TAB
    IMP_IO    = TAB + LF
    IMP_FLOW  = LF

    def run(self, program: str, input_stream: str = "") -> str:
        code = "".join(ch for ch in program if ch in (self.SPACE, self.TAB, self.LF))
        self.input_stream = input_stream
        self.inp_ptr = 0
        self.output = []

        instructions, label_pos = self._parse(code)

        stack = []
        heap = {}
        call_stack = []
        pc = 0
        halted = False

        def pop():
            if not stack:
                raise WhitespaceError("Stack underflow")
            return stack.pop()

        while 0 <= pc < len(instructions):
            op, arg = instructions[pc]
            pc += 1
            imp, sub = op

            # STACK
            if imp == self.IMP_STACK:
                if sub == (self.SPACE,):  # push number
                    n = arg
                    if n is None:
                        raise WhitespaceError("Invalid number literal")
                    stack.append(n)
                elif sub == (self.TAB, self.SPACE):  # copy nth
                    n = arg
                    if n is None or n < 0 or n >= len(stack):
                        raise WhitespaceError("Invalid stack access for copy")
                    stack.append(stack[-1 - n])
                elif sub == (self.TAB, self.LF):  # discard n below top
                    n = arg
                    if len(stack) <= 1:
                        continue
                    if n is None or n < 0 or n >= len(stack):
                        top = stack[-1]
                        stack[:] = [top]
                    else:
                        top = stack.pop()
                        if n > 0:
                            del stack[-n:]
                        stack.append(top)
                elif sub == (self.LF, self.SPACE):  # dup
                    if not stack:
                        raise WhitespaceError("Stack underflow on dup")
                    stack.append(stack[-1])
                elif sub == (self.LF, self.TAB):  # swap
                    if len(stack) < 2:
                        raise WhitespaceError("Need two values to swap")
                    stack[-1], stack[-2] = stack[-2], stack[-1]
                elif sub == (self.LF, self.LF):  # pop
                    if not stack:
                        raise WhitespaceError("Stack underflow on pop")
                    stack.pop()
                else:
                    raise WhitespaceError("Unknown stack instruction")

            # ARITH
            elif imp == self.IMP_ARITH:
                if len(stack) < 2:
                    raise WhitespaceError("Need two values for arithmetic")
                a = pop()
                b = pop()
                if sub == (self.SPACE, self.SPACE):      # add
                    stack.append(b + a)
                elif sub == (self.SPACE, self.TAB):      # sub
                    stack.append(b - a)
                elif sub == (self.SPACE, self.LF):       # mul
                    stack.append(b * a)
                elif sub == (self.TAB, self.SPACE):      # div (floor)
                    if a == 0:
                        raise WhitespaceError("Division by zero")
                    stack.append(b // a)
                elif sub == (self.TAB, self.TAB):        # mod
                    if a == 0:
                        raise WhitespaceError("Modulo by zero")
                    stack.append(b % a)
                else:
                    raise WhitespaceError("Unknown arithmetic instruction")

            # HEAP
            elif imp == self.IMP_HEAP:
                if sub == (self.SPACE,):  # store
                    if len(stack) < 2:
                        raise WhitespaceError("Need two values to store")
                    a = pop()
                    b = pop()
                    heap[b] = a
                elif sub == (self.TAB,):  # load
                    if not stack:
                        raise WhitespaceError("Need address to load")
                    a = pop()
                    if a not in heap:
                        raise WhitespaceError("Invalid heap address")
                    stack.append(heap[a])
                else:
                    raise WhitespaceError("Unknown heap instruction")

            # IO
            elif imp == self.IMP_IO:
                if sub == (self.SPACE, self.SPACE):  # output char
                    if not stack:
                        raise WhitespaceError("Stack underflow on putchar")
                    a = pop()
                    self.output.append(chr(a & 0xFF))
                elif sub == (self.SPACE, self.TAB):  # output number
                    if not stack:
                        raise WhitespaceError("Stack underflow on putnum")
                    a = pop()
                    self.output.append(str(a))
                elif sub == (self.TAB, self.SPACE):  # read char
                    if not stack:
                        raise WhitespaceError("Need address to read char")
                    addr = pop()
                    ch = self._read_char()
                    heap[addr] = ord(ch)
                elif sub == (self.TAB, self.TAB):    # read number
                    if not stack:
                        raise WhitespaceError("Need address to read number")
                    addr = pop()
                    num = self._read_number()
                    heap[addr] = num
                else:
                    raise WhitespaceError("Unknown IO instruction")

            # FLOW
            elif imp == self.IMP_FLOW:
                if sub == (self.SPACE, self.SPACE):  # mark
                    pass
                elif sub == (self.SPACE, self.TAB):  # call
                    label = arg
                    if label not in label_pos:
                        raise WhitespaceError("Undefined label in call")
                    call_stack.append(pc)
                    pc = label_pos[label]
                elif sub == (self.SPACE, self.LF):   # jump
                    label = arg
                    if label not in label_pos:
                        raise WhitespaceError("Undefined label in jump")
                    pc = label_pos[label]
                elif sub == (self.TAB, self.SPACE):  # jz
                    if not stack:
                        raise WhitespaceError("Stack underflow on jz")
                    v = pop()
                    label = arg
                    if label not in label_pos:
                        raise WhitespaceError("Undefined label in jz")
                    if v == 0:
                        pc = label_pos[label]
                elif sub == (self.TAB, self.TAB):    # jn
                    if not stack:
                        raise WhitespaceError("Stack underflow on jn")
                    v = pop()
                    label = arg
                    if label not in label_pos:
                        raise WhitespaceError("Undefined label in jn")
                    if v < 0:
                        pc = label_pos[label]
                elif sub == (self.TAB, self.LF):     # return
                    if not call_stack:
                        raise WhitespaceError("Return with empty call stack")
                    pc = call_stack.pop()
                elif sub == (self.LF, self.LF):      # end
                    halted = True
                    break
                else:
                    raise WhitespaceError("Unknown flow instruction")
            else:
                raise WhitespaceError("Unknown instruction group")

        if not halted:
            raise WhitespaceError("Program did not terminate cleanly")
        return "".join(self.output)

    # -------- parsing helpers --------
    def _parse(self, code: str):
        i = 0
        n = len(code)
        instructions = []
        label_pos = {}

        def need(k=1):
            if i + k > n:
                raise WhitespaceError("Unexpected end of program")

        def read_number():
            nonlocal i
            need(1)
            if code[i] == self.LF:
                raise WhitespaceError("Invalid number literal (missing sign)")
            sign = code[i]
            if sign not in (self.SPACE, self.TAB):
                raise WhitespaceError("Invalid number sign")
            i += 1
            bits = []
            while True:
                need(1)
                c = code[i]
                i += 1
                if c == self.LF:
                    break
                if c == self.SPACE:
                    bits.append("0")
                elif c == self.TAB:
                    bits.append("1")
                else:
                    raise WhitespaceError("Invalid digit in number")
            if len(bits) == 0:
                value = 0
            else:
                value = int("".join(bits), 2)
                if sign == self.TAB:
                    value = -value
            return value

        def read_label():
            nonlocal i
            chars = []
            while True:
                need(1)
                c = code[i]
                i += 1
                if c == self.LF:
                    break
                if c in (self.SPACE, self.TAB):
                    chars.append(c)
                else:
                    raise WhitespaceError("Invalid char in label")
            return "".join(chars)

        while i < n:
            need(1)
            c = code[i]; i += 1
            if c == self.SPACE:
                imp = self.IMP_STACK
                need(1)
                c2 = code[i]; i += 1
                if c2 == self.SPACE:
                    sub = (self.SPACE,)
                    num = read_number()
                    instructions.append(((imp, sub), num))
                elif c2 == self.TAB:
                    need(1)
                    c3 = code[i]; i += 1
                    if c3 == self.SPACE:
                        sub = (self.TAB, self.SPACE)
                        num = read_number()
                        instructions.append(((imp, sub), num))
                    elif c3 == self.LF:
                        sub = (self.TAB, self.LF)
                        num = read_number()
                        instructions.append(((imp, sub), num))
                    else:
                        raise WhitespaceError("Unknown stack TAB-* op")
                elif c2 == self.LF:
                    need(1)
                    c3 = code[i]; i += 1
                    if c3 == self.SPACE:
                        sub = (self.LF, self.SPACE)
                        instructions.append(((imp, sub), None))
                    elif c3 == self.TAB:
                        sub = (self.LF, self.TAB)
                        instructions.append(((imp, sub), None))
                    elif c3 == self.LF:
                        sub = (self.LF, self.LF)
                        instructions.append(((imp, sub), None))
                    else:
                        raise WhitespaceError("Unknown stack LF-* op")
                else:
                    raise WhitespaceError("Unknown stack op")

            elif c == self.TAB:
                need(1)
                c2 = code[i]; i += 1
                if c2 == self.SPACE:
                    imp = self.IMP_ARITH
                    need(1); a = code[i]; i += 1
                    need(1); b = code[i]; i += 1
                    sub = (a, b)
                    if sub not in {
                        (self.SPACE, self.SPACE),
                        (self.SPACE, self.TAB),
                        (self.SPACE, self.LF),
                        (self.TAB, self.SPACE),
                        (self.TAB, self.TAB),
                    }:
                        raise WhitespaceError("Unknown arithmetic op")
                    instructions.append(((imp, sub), None))
                elif c2 == self.TAB:
                    imp = self.IMP_HEAP
                    need(1); c3 = code[i]; i += 1
                    if c3 == self.SPACE:
                        sub = (self.SPACE,)
                    elif c3 == self.TAB:
                        sub = (self.TAB,)
                    else:
                        raise WhitespaceError("Unknown heap op")
                    instructions.append(((imp, sub), None))
                elif c2 == self.LF:
                    imp = self.IMP_IO
                    need(1); a = code[i]; i += 1
                    need(1); b = code[i]; i += 1
                    sub = (a, b)
                    if sub not in {
                        (self.SPACE, self.SPACE),
                        (self.SPACE, self.TAB),
                        (self.TAB, self.SPACE),
                        (self.TAB, self.TAB),
                    }:
                        raise WhitespaceError("Unknown IO op")
                    instructions.append(((imp, sub), None))
                else:
                    raise WhitespaceError("Unknown TAB-* group")

            elif c == self.LF:
                imp = self.IMP_FLOW
                need(1)
                c2 = code[i]; i += 1
                if c2 == self.SPACE:
                    need(1)
                    c3 = code[i]; i += 1
                    if c3 == self.SPACE:
                        sub = (self.SPACE, self.SPACE)
                        label = read_label()
                        if label in label_pos:
                            raise WhitespaceError("Duplicate label")
                        label_pos[label] = len(instructions)
                        instructions.append(((imp, sub), label))
                    elif c3 == self.TAB:
                        sub = (self.SPACE, self.TAB)
                        label = read_label()
                        instructions.append(((imp, sub), label))
                    elif c3 == self.LF:
                        sub = (self.SPACE, self.LF)
                        label = read_label()
                        instructions.append(((imp, sub), label))
                    else:
                        raise WhitespaceError("Unknown LF SPACE-* flow")
                elif c2 == self.TAB:
                    need(1)
                    c3 = code[i]; i += 1
                    if c3 == self.SPACE:
                        sub = (self.TAB, self.SPACE)
                        label = read_label()
                        instructions.append(((imp, sub), label))
                    elif c3 == self.TAB:
                        sub = (self.TAB, self.TAB)
                        label = read_label()
                        instructions.append(((imp, sub), label))
                    elif c3 == self.LF:
                        sub = (self.TAB, self.LF)
                        instructions.append(((imp, sub), None))
                    else:
                        raise WhitespaceError("Unknown LF TAB-* flow")
                elif c2 == self.LF:
                    need(1)
                    c3 = code[i]; i += 1
                    if c3 == self.LF:
                        sub = (self.LF, self.LF)
                        instructions.append(((imp, sub), None))
                    else:
                        raise WhitespaceError("Unknown LF LF-* flow")
                else:
                    raise WhitespaceError("Unknown LF-* group")
            else:
                raise WhitespaceError("Unknown IMP")

        return instructions, label_pos

    # -------- input helpers --------
    def _read_char(self) -> str:
        if self.inp_ptr >= len(self.input_stream):
            raise WhitespaceError("Unexpected end of input (char)")
        ch = self.input_stream[self.inp_ptr]
        self.inp_ptr += 1
        return ch

    def _read_number(self) -> int:
        if self.inp_ptr >= len(self.input_stream):
            raise WhitespaceError("Unexpected end of input (number)")
        j = self.input_stream.find("\n", self.inp_ptr)
        if j == -1:
            raise WhitespaceError("Missing newline terminator for number")
        token = self.input_stream[self.inp_ptr:j]
        self.inp_ptr = j + 1
        try:
            return int(token, 0)  # accepts 0x..., 0b..., 0o..., decimal
        except ValueError:
            raise WhitespaceError(f"Invalid integer input: {token!r}")


def whitespace(code: str, input: str = "") -> str:
    """
    Execute a Whitespace program.
    - code: string containing the program (whitespace may be interleaved with comments).
    - input: input stream (characters and/or newline-terminated integers).
    Returns the output as a string.
    """
    return _WhitespaceVM().run(code, input)