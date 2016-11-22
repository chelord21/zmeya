class Memory(object):
    """ Memory class

    One memory object, which has an array of memory objects and the last quadruple processed.
    """
    def __init__(self):
        self.memory = []
        self.last_quadruple = None

    def build(self, memory, last_quadruple):
        """Build Memory

        Generates one memory object
        """
        self.memory = memory
        self.last_quadruple = last_quadruple
