from .registers import REGISTERS, is_register
from .memory import MEMORY, is_memory_loc, to_memory_loc


def is_immediate(op):
    return op.startswith('$')


def to_int(op):
    return int(op.removeprefix('$'))


def resolve(op):
    """Resolves the operand

    Fetches the value or convert it depending on the operand type.
    """
    if is_register(op):
        return REGISTERS[op]
    elif is_memory_loc(op):
        return MEMORY[to_memory_loc(op)]
    elif is_immediate(op):
        return to_int(op)
