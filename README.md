# RISC
A Reduced Instruction Set Computer written in Python.

## Usage
First unzip the project
```
unzip risc.zip
```

Create a virtual environment and activate it
```
python3 -m venv venv
source venv/bin/activate
```

Install the package to have access to the `risc` command
```
python3 setup.py install
```

Run the examples
```
risc examples/fiboacci.risc
```

## Running Tests
To be able to run the test, you should install in the `dev` mode
```
pip install -e .[dev]
```

**NOTE**: The `dev` mode has conflict with the `prod` mode. If you install
using the `dev` mode, you can have the `risc` command and the tests at the same
time.

To run the test suit
```
pytest tests
```

## Running Linter
To be able to run the linter, you should install in the `dev` mode.

To run the linter
```
flake8 risc tests
```

## Architecture
There are two main components:
* The parser which parses a source code and returns an internal representation
  which can be run by the `risc` virtual machine similar to bytecodes in the
  programming languages
* The virtual machine which runs the internal representation. It has 4 general
  purpose registers (data registers), status registers and 1KiB of random
  access memory.

## RISC Syntax
`risc` programs are written in a syntax similar to AT&T syntax which is widely
used in the UNIX systems.

An instruction has the form of
```
mnemonic op1 op2
```
in which either `op1` or `op2` or both can be omitted depending on the
instruction. For instance, `ADD` has 2 operands, `JMP` has one and `HALT` has
zero operands.

`risc` also supports labels by which loops and conditionals can be implemented.
A label is defined as follows
```
lable:
```

Registers are prefixed with `%` (like the AT&T syntax) and memory locations are
prefixed with `#` (it doesn't exist in the AT&T). Immediate values are prefixed
with `$` (again like the AT&T).

See the `examples` directory for practical examples.

## Main Features
To ease the reviewing of the code, in the following lines, I have highlighted
the main features of `risc`.

The parser has 3 phases or passes similar to what is found in modern compilers.

The parser can handle basic syntax errors and reports them with their line number.

Each register is implemented as an integer. Registers in reality have fixed
length but Python integers have no length.

The memory is an array of integers. Again integers in Python have no length.

The status registers are implemented as integers. In reality there is one
status register in which each bit has a specific meaning. Since bitwise
arithmetic in Python are not straightforward, I chose this implementation.

When a `risc` program ran successfully, the state of the registers are printed
so that one can get the actual result and verify it.

All of the instruction have unit tests. There are also some integration tests
which run some sample programs on the VM.

## The Optional Tasks
1. Write some tests for the machine and a test harness that checks that these
   tests pass:

   See the `tests` folder.
2. Write some programs (fib, factorial, sum) for the RISC machine:

   See the `examples` folder.
4. Design a binary encoding for the instruction set. Get your RISC machine to
   decode and then execute the program:

   A binary representation similar to x86's can be used.
5. Extend the instruction set with other arithmetic and logical instructions:

   There are `MUL` and several conditional jumps available. See the source
   code.
