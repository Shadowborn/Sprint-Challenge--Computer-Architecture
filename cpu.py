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
    #INITALIZE OPERATION CODES
        self.op_codes = {
            'PUSH': 0b01000101,
            'POP': 0b01000110,
            'ADD': 0b10100000,
            'JEQ': 0b01010101,
            'JNE': 0b01010110,
            'JMP': 0b01010100,
            'CMP': 0b10100111,
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'HLT': 0b00000001,
            'MUL': 0b10100010,
            'CALL': 0b01010000,
            'RET': 0b00010001,
        }
        #set flag to my ls-8
        self.flag = 0b0000000 
