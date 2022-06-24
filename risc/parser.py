import sys

from .instructions import Instruction, is_instruction
from .labels import Label, is_label


class Fragment:
    def __init__(self, line, line_num):
        self.tokens = [li.strip() for li in line.split()]
        self.orig_line = line
        self.line_num = line_num

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)

    def __str__(self):
        return '{}(tokens={})'.format(self.__class__.__name__, self.tokens)

    def __repr__(self):
        return '<{}(tokens={})>'.format(self.__class__.__name__, self.tokens)


def parse_phase_1(input):
    """The first parsing phase

    Splits the input into a list of lines
    """
    return [line.strip() for line in input.splitlines()]


def parse_phase_2(lines):
    """The second parsing phase

    Parses each line and returns a program and labels
    """
    loc = 0  # Location counter
    labels = {}
    program = []
    for line_num, line in enumerate(lines, start=1):
        if not line:
            continue

        fragment = Fragment(line, line_num)
        if is_instruction(fragment[0]):
            instruction = Instruction(fragment)
            program.append(instruction)
            loc += 1
        elif is_label(fragment[0]):
            label = Label(fragment[0].strip(':'), loc)
            labels[label.name] = label
        else:
            raise SyntaxError(
                'Syntax error at line: {}\n{}'.format(
                    fragment.line_num, fragment.orig_line
                )
            )
    return program, labels


def parse_phase_3(program, labels):
    """The third parsing phase

    Finds the instructions with location and replaces
    the location with a relative address.
    """
    result = []
    for inst in program:
        if inst.has_label():
            inst.op1 = labels[inst.op1]
        result.append(inst)
    return result


def parse(input):
    """Runs each phase of parsing and returns a runnable program"""
    try:
        lines = parse_phase_1(input)
        program, labels = parse_phase_2(lines)
        program = parse_phase_3(program, labels)
    except SyntaxError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    return program
