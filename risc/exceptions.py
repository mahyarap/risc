class NoSuchInstruction(Exception):
    pass


class EndOfProgram(Exception):
    """Used by the HALT instruction"""
