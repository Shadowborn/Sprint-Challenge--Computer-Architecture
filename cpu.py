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
        self.im = 5
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

    def load(self, file):
        address = 0

        program = []

        if file is None:
            print("ERROR: The file is not working")
            sys.exit(1)

        try:
            with open(file, 'r') as f:
                for line in f:
                    split_comment = line.split('#')
                    number = split_comment[0]

                    try:
                        x = int(number, 2)
                    except ValueError:
                        continue
                    print(f"{x:08b}: {x:d}")
                    program.append(x)
        except ValueError:
            print(f"File not found")

        for instructions in program:
            self.ram[address] = instructions
            address += 1

    def jmp(self, address, *args):
        self.pc = self.register[address]

    def jeq(self, address, *args):
        mask = 0b00000001
        if mask & self.im == 1:
            self.pc = self.register[address]
        else:
            self.pc += 2

    def jne(self, address, *args):
        mask = 0b00000001
        if mask & self.im == 0:
            self.pc = self.register[address]
        else:
            self.pc += 2

    def alu(self, op, reg_a, reg_b):

        # mask == 0b00000001

        # if op == self.op_codes['JMP']:
        #     self.pc = self.register[address]

        # if op == self.op_codes['JEQ']:
        #     if mask & self.im == 1:
        #         self.pc = self.register[address]
        #     else:
        #         self.pc += 2

        # if op == self.op_codes['JNE']:
        #     if mask & self.im == 0:
        #         self.pc = self.register[address]
        #     else:
        #         self.pc += 2

        if op == self.op_codes['ADD']:
            self.register[reg_a] += self.register[reg_b]
            self.pc += 3
        
        elif op == self.op_codes['MUL']:
            self.register[reg_a] *= self.register[reg_b]
            self.pc += 3

        elif op == self.op_codes['CMP']:
            
            if reg_a == reg_b:  # if a == b, set E to 1
                self.flag = 0b00000001

            elif reg_a < reg_b:  # if a < b, set L to 1
                self.flag = 0b00000100

            elif reg_a > reg_b:  # if a > b, set G to 1
                self.flag = 0b00000010

        else:
            raise Exception("Unsupported ALU operation")
        
