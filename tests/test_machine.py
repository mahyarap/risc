from risc.parser import parse
from risc.machine import run
from risc.registers import REGISTERS


def test_add_two_numbers():
    sample = """
    load $2 %AX
    load $3 %BX
    add %BX %AX
    """
    program = parse(sample)
    retval = run(program)
    assert retval == 0
    assert REGISTERS['%AX'] == 5


def test_subtract_two_numbers():
    sample = """
    load $2 %AX
    load $3 %BX
    sub %BX %AX
    """
    program = parse(sample)
    retval = run(program)
    assert retval == 0
    assert REGISTERS['%AX'] == -1


def test_jump_to_label():
    sample = """
    load $2 %AX
    jmp end
    load $3 %AX
    end:
      halt
    """
    program = parse(sample)
    retval = run(program)
    assert retval == 0
    assert REGISTERS['%AX'] == 2


def test_jump_condition_true():
    sample = """
    load $2 %AX
    load $2 %BX
    cmp %BX %AX
    je loc1
    jmp end
    loc1:
      load $0 %AX
    end:
      halt
    """
    program = parse(sample)
    retval = run(program)
    assert retval == 0
    assert REGISTERS['%AX'] == 0


def test_jump_condition_false():
    sample = """
    load $2 %AX
    load $3 %BX
    cmp %BX %AX
    je loc1
    jmp end
    loc1:
      load $0 %AX
    end:
      halt
    """
    program = parse(sample)
    retval = run(program)
    assert retval == 0
    assert REGISTERS['%AX'] == 2


def test_simple_loop():
    """
    for (int i = 2; i > 0; i--) {}
    """
    sample = """
    load $2 %AX
    jmp loc1
    loop:
      sub $1 %AX
    loc1:
      cmp $0 %AX
      jg loop
    """
    program = parse(sample)
    retval = run(program)
    assert retval == 0
    assert REGISTERS['%AX'] == 0
