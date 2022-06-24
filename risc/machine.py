from .instructions import (
    InstructionSet, add, sub, mul, cmp, load, store, jmp, je, jg, jl, halt
)
from .exceptions import NoSuchInstruction, EndOfProgram
from .registers import PC, REGISTERS, FLAGS  # noqa


ISET = InstructionSet  # For convenience


def run(program):
    """Runs a runnable program

    Runs the program until the end of instructions or terminates early if a
    HALT is encountered.
    """
    global PC
    PC = 0
    try:
        while PC < len(program):
            inst = program[PC]
            if inst.name == ISET.NOP.value:
                PC += 1
            elif inst.name == ISET.LOAD.value:
                load(inst.op1, inst.op2)
                PC += 1
            elif inst.name == ISET.STORE.value:
                store(inst.op1, inst.op2)
                PC += 1
            elif inst.name == ISET.ADD.value:
                add(inst.op1, inst.op2)
                PC += 1
            elif inst.name == ISET.SUB.value:
                sub(inst.op1, inst.op2)
                PC += 1
            elif inst.name == ISET.MUL.value:
                mul(inst.op1, inst.op2)
                PC += 1
            elif inst.name == ISET.CMP.value:
                cmp(inst.op1, inst.op2)
                PC += 1
            elif inst.name == ISET.JMP.value:
                PC = jmp(inst.op1)
            elif inst.name == ISET.JE.value:
                cond, loc = je(inst.op1)
                if cond:
                    PC = loc
                else:
                    PC += 1
            elif inst.name == ISET.JG.value:
                cond, loc = jg(inst.op1)
                if cond:
                    PC = loc
                else:
                    PC += 1
            elif inst.name == ISET.JL.value:
                cond, loc = jl(inst.op1)
                if cond:
                    PC = loc
                else:
                    PC += 1
            elif inst.name == ISET.HALT.value:
                halt()
            else:
                raise NoSuchInstruction(inst)
        return 0
    except EndOfProgram:
        return 0


def print_state():
    output = """
REGISTERS:
    %AX: {ax}, %BX: {bx}, %CX: {cx}, %DX: {dx}

FLAGS:
    ZF: {zf}, CF: {cf}
    """.format(
        ax=REGISTERS['%AX'],
        bx=REGISTERS['%BX'],
        cx=REGISTERS['%CX'],
        dx=REGISTERS['%DX'],
        zf=FLAGS['ZF'],
        cf=FLAGS['CF']
    )
    print(output)
