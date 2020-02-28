import sys

class myCPU:

    def __init__(self):
        # Create registers 0 - 7
        self.register = [0] * 8
        # Create a program counter
        self.pc = 0
        # Create insruction register
        self.IR = 0
        # initialize RAM space
        self.ram = [0] * 256
        # Create stack pointer
        self.SP = 7
        