import sys

class myCPU:
    print(f"Helloooo start of myCPU")
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
        print(f"Loading file...")
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

    def alu(self, op, reg_a, reg_b):

        if op == self.op_codes['JMP']:
            self.pc = self.register

        if op == self.op_codes['JEQ']:
            if self.im == 1:
                self.pc = self.register
            else:
                self.pc += 2

        if op == self.op_codes['JNE']:
            if self.im == 0:
                self.pc = self.register
            else:
                self.pc += 2

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

    def trace(self):

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()
    def run(self):
        running = True

        while running:

            # Instruction register, contains a copy of the currently executing instruction
            IR = self.ram[self.pc]

            if IR == self.op_codes['LDI']:  # LDI
                num = self.ram[self.pc + 1]
                register = self.ram[self.pc + 2]

                self.register[num] = register
                self.pc += 3

            elif IR == self.op_codes['PRN']:  # PRN
                register = self.ram[self.pc + 1]
                print(self.register[register])
                self.pc += 2

            elif IR == self.op_codes['HLT']:  # HLT
                running = False
                self.pc += 1

            elif IR == self.op_codes['PUSH']:
                register = self.ram[self.pc + 1]
                val = self.register[register]
                #  Got to decrement the Stack pointer.
                self.register[self.SP] -= 1
                # Copy the value in the given register to the address pointed to by Stack pointer
                self.ram[self.register[self.SP]] = val
                self.pc += 2

            elif IR == self.op_codes['POP']:
                register = self.ram[self.pc + 1]
                val = self.ram[self.register[self.SP]]
                # Copy the value from the address pointed to by Stack pointer to the given register
                self.register[register] = val
                # Increment SP
                self.register[self.SP] += 1
                self.pc += 2

            elif IR == self.op_codes['CALL']:
                # we want to push the return address on the stack
                self.register[self.SP] -= 1  # the stack push
                self.ram[self.register[self.SP]] = self.pc + 2

                # The program counter is set to the address stored in the given register
                register = self.ram[self.pc + 1]
                # We then jump to that location in the RAM and execute the first instruction
                self.pc = self.register[register]

            elif IR == self.op_codes['RET']:
                # return the subroutine
                self.pc = self.ram[self.register[self.SP]]
                # pop the value from the top of the stack
                self.register[self.SP] += 1

            elif IR == self.op_codes['ADD']:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu(IR, reg_a, reg_b)

            elif IR == self.op_codes['MUL']:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu(IR, reg_a, reg_b)

            elif IR == self.op_codes['CMP']:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu(IR, reg_a, reg_b)

            else:
                print(f"Unknown IR: {IR}")
                sys.exit(1)

    def ram_read(self, MAR):
        # Read from RAM
        # Accepts the address to read and return the value stored there
        return self.ram[MAR]

    # accept a value to write, and the addres to write it to
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        
