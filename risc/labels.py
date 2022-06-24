class Label:
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc

    def __str__(self):
        return '{}(name={}, loc={})'.format(
            self.__class__.__name__,
            self.name,
            self.loc
        )

    def __repr__(self):
        return '<{}(name={}, loc={})>'.format(
            self.__class__.__name__,
            self.name,
            self.loc
        )


def is_label(op):
    return op.endswith(':')
