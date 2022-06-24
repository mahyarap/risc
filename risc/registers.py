# The general purpose registers AKA the data registers
REGISTERS = {
    '%AX': 0,
    '%BX': 0,
    '%CX': 0,
    '%DX': 0,
}

# The FLAGS register AKA the status register
FLAGS = {
    'ZF': 0,
    'CF': 0,
}

# The program counter register (It's not exposed to the user)
PC = 0


def is_register(op):
    return op in REGISTERS
