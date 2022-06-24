# 1 KiB fixed memory
MEMORY = [0] * 2**10


def is_memory_loc(op):
    return op.startswith('#')


def to_memory_loc(op):
    return int(op.removeprefix('#'))
