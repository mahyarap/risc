from enum import Enum

from .memory import MEMORY, is_memory_loc, to_memory_loc
from .registers import REGISTERS, FLAGS, is_register
from .utils import resolve
from .exceptions import EndOfProgram


class InstructionSet(Enum):
    NOP = 'NOP'
    LOAD = 'LOAD'
    STORE = 'STORE'
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    CMP = 'CMP'
    JMP = 'JMP'
    JE = 'JE'
    JG = 'JG'
    JL = 'JL'
    HALT = 'HALT'


INSTRUCTIONS = {inst.value for inst in InstructionSet}


def is_instruction(op):
    return op.upper() in INSTRUCTIONS


class Instruction:
    def __init__(self, fragment):
        if len(fragment) == 3:
            name, op1, op2 = fragment
        elif len(fragment) == 2:
            name, op1 = fragment
            op2 = None
        elif len(fragment) == 1:
            name = fragment[0]
            op1 = None
            op2 = None
        else:
            raise SyntaxError(
                'Syntax error at line: {}\n{}'.format(
                    fragment.line_num, fragment.orig_line
                )
            )
        self.name = name.upper()
        self.op1 = op1
        self.op2 = op2

    def has_label(self):
        return self.name in {
            InstructionSet.JMP.value,
            InstructionSet.JE.value,
            InstructionSet.JG.value,
            InstructionSet.JL.value,
        }

    def __str__(self):
        return '{}(name={}, op1={}, op2={})'.format(
            self.__class__.__name__,
            self.name.upper(),
            self.op1,
            self.op2
        )

    def __repr__(self):
        return '<{}(name={}, op1={}, op2={})>'.format(
            self.__class__.__name__,
            self.name.upper(),
            self.op1,
            self.op2
        )


def add(src, dst):
    if is_register(dst):
        REGISTERS[dst] += resolve(src)
    elif is_memory_loc(dst):
        MEMORY[to_memory_loc(dst)] += resolve(src)


def sub(src, dst):
    if is_register(dst):
        REGISTERS[dst] -= resolve(src)
    elif is_memory_loc(dst):
        MEMORY[to_memory_loc(dst)] -= resolve(src)


def mul(src, dst):
    if is_register(dst):
        REGISTERS[dst] *= resolve(src)
    elif is_memory_loc(dst):
        MEMORY[to_memory_loc(dst)] *= resolve(src)


def load(src, dst):
    REGISTERS[dst] = resolve(src)


def store(src, dst):
    MEMORY[to_memory_loc(dst)] = resolve(src)


def halt():
    raise EndOfProgram


def nop():
    pass


def cmp(src, dst):
    result = resolve(dst) - resolve(src)
    if result > 0:
        FLAGS['CF'] = 0
        FLAGS['ZF'] = 0
    elif result < 0:
        FLAGS['CF'] = 1
        FLAGS['ZF'] = 0
    else:
        FLAGS['CF'] = 0
        FLAGS['ZF'] = 1


def jmp(dst):
    return dst.loc


def je(dst):
    if FLAGS['CF'] == 0 and FLAGS['ZF'] == 1:
        return True, dst.loc
    return False, 0


def jg(dst):
    if FLAGS['CF'] == 0 and FLAGS['ZF'] == 0:
        return True, dst.loc
    return False, 0


def jl(dst):
    if FLAGS['CF'] == 1 and FLAGS['ZF'] == 0:
        return True, dst.loc
    return False, 0
