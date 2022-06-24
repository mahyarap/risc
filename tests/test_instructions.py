import pytest

from risc.instructions import (
    add, load, sub, mul, store, cmp, halt, jmp, je, jg, jl
)
from risc.registers import REGISTERS, FLAGS
from risc.memory import MEMORY
from risc.labels import Label
from risc.exceptions import EndOfProgram


@pytest.fixture
def reset_memory():
    for i in range(len(MEMORY)):
        MEMORY[i] = 0
    yield
    for i in range(len(MEMORY)):
        MEMORY[i] = 0


@pytest.fixture
def reset_registers():
    for reg in REGISTERS:
        REGISTERS[reg] = 0
    yield
    for reg in REGISTERS:
        REGISTERS[reg] = 0


@pytest.fixture
def reset_eflags():
    for flag in FLAGS:
        FLAGS[flag] = 0
    yield
    for flag in FLAGS:
        FLAGS[flag] = 0


class TestLoad:
    def test_load_immeidate(self):
        load('$2', '%AX')
        assert REGISTERS['%AX'] == 2

    def test_load_memory(self):
        MEMORY[3] = 6
        load('#3', '%AX')
        assert REGISTERS['%AX'] == 6


class TestStore:
    def test_store_immeidate(self):
        store('$2', '#0')
        assert MEMORY[0] == 2

    def test_store_register(self):
        MEMORY[3] = 6
        store('#3', '#0')
        assert MEMORY[0] == 6


class TestAdd:
    def test_add_immediate_register(self, reset_registers):
        add('$1', '%AX')
        assert REGISTERS['%AX'] == 1

    def test_add_memory_register(self, reset_registers):
        MEMORY[0] = 2
        MEMORY[1] = 3
        load('#0', '%AX')
        add('#1', '%AX')
        assert REGISTERS['%AX'] == 5

    def test_add_register_register(self, reset_registers):
        load('$2', '%AX')
        load('$3', '%BX')
        add('%BX', '%AX')
        assert REGISTERS['%AX'] == 5

    def test_add_immediate_memory(self, reset_registers):
        MEMORY[2] = 3
        add('$1', '#2')
        assert MEMORY[2] == 4

    def test_add_memory_memory(self, reset_registers):
        MEMORY[1] = 2
        MEMORY[2] = 3
        add('#1', '#2')
        assert MEMORY[2] == 5


class TestSub:
    def test_sub_immediate_register(self, reset_registers):
        sub('$1', '%AX')
        assert REGISTERS['%AX'] == -1

    def test_sub_memory_register(self, reset_registers):
        MEMORY[0] = 2
        MEMORY[1] = 3
        load('#0', '%AX')
        sub('#1', '%AX')
        assert REGISTERS['%AX'] == -1

    def test_sub_register_register(self, reset_registers):
        load('$2', '%AX')
        load('$3', '%BX')
        sub('%BX', '%AX')
        assert REGISTERS['%AX'] == -1

    def test_sub_immediate_memory(self, reset_registers):
        MEMORY[2] = 3
        sub('$1', '#2')
        assert MEMORY[2] == 2

    def test_sub_memory_memory(self, reset_registers):
        MEMORY[1] = 2
        MEMORY[2] = 3
        sub('#1', '#2')
        assert MEMORY[2] == 1


class TestMul:
    def test_mul_immediate_register(self, reset_registers):
        mul('$5', '%AX')
        assert REGISTERS['%AX'] == 0

    def test_mul_memory_register(self, reset_registers):
        MEMORY[0] = 2
        MEMORY[1] = 3
        load('#0', '%AX')
        mul('#1', '%AX')
        assert REGISTERS['%AX'] == 6

    def test_mul_register_register(self, reset_registers):
        load('$2', '%AX')
        load('$3', '%BX')
        mul('%BX', '%AX')
        assert REGISTERS['%AX'] == 6

    def test_mul_immediate_memory(self, reset_registers):
        MEMORY[2] = 3
        mul('$1', '#2')
        assert MEMORY[2] == 3

    def test_mul_memory_memory(self, reset_registers):
        MEMORY[1] = 2
        MEMORY[2] = 3
        mul('#1', '#2')
        assert MEMORY[2] == 6


class TestCmp:
    def test_cmp_register_register_same(self, reset_eflags):
        load('$1', '%AX')
        load('$1', '%BX')
        cmp('%AX', '%BX')
        assert FLAGS['CF'] == 0
        assert FLAGS['ZF'] == 1

    def test_cmp_register_register_greater(self, reset_eflags):
        load('$1', '%AX')
        load('$2', '%BX')
        cmp('%AX', '%BX')
        assert FLAGS['CF'] == 0
        assert FLAGS['ZF'] == 0

    def test_cmp_register_register_less(self, reset_eflags):
        load('$2', '%AX')
        load('$1', '%BX')
        cmp('%AX', '%BX')
        assert FLAGS['CF'] == 1
        assert FLAGS['ZF'] == 0


class TestHalt:
    def test_halt(self):
        with pytest.raises(EndOfProgram):
            halt()


class TestJmp:
    def test_jmp(self):
        assert jmp(Label('loc', 3)) == 3

    def test_je_true(self):
        load('$1', '%AX')
        load('$1', '%BX')
        cmp('%AX', '%BX')
        assert je(Label('loc', 3)) == (True, 3)

    def test_je_false(self):
        load('$1', '%AX')
        load('$2', '%BX')
        cmp('%AX', '%BX')
        assert je(Label('loc', 3)) == (False, 0)

    def test_jg_true(self):
        load('$1', '%AX')
        load('$2', '%BX')
        cmp('%AX', '%BX')
        assert jg(Label('loc', 3)) == (True, 3)

    def test_jg_false(self):
        load('$2', '%AX')
        load('$1', '%BX')
        cmp('%AX', '%BX')
        assert jg(Label('loc', 3)) == (False, 0)

    def test_jl_true(self):
        load('$2', '%AX')
        load('$1', '%BX')
        cmp('%AX', '%BX')
        assert jl(Label('loc', 3)) == (True, 3)

    def test_jl_false(self):
        load('$1', '%AX')
        load('$2', '%BX')
        cmp('%AX', '%BX')
        assert jl(Label('loc', 3)) == (False, 0)
