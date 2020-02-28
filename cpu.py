import sys

# #Op_codes
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
ST = 0b10000100
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


# Register for Stack Pointer
SP = 7 

class myCPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        """ Ram holding 256 bytes of memory """
        self.ram = [0] * 256
        """ Reg holding 8 positions """
        self.reg = [0] * 8
        """ program control """
        self.pc = 0
        """ Start the stack pointer at F4 """
        self.reg[SP] = 0xf4 # F4 of the stack
        self.FL = 0

        """ 
        `FL` bits: `00000LGE`
        * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
        zero otherwise.
        * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
        registerB, zero otherwise.
        * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
        otherwise.
        """
        self.FLLT = 0b0000100 # Less_than flag
        self.FLGT = 0b0000010 # Greater_than flag
        self.FLET = 0b0000001 # Equal_to flag
        self.running = True 
       
        # BranchTable
        self.branchtable = {}
        self.branchtable[LDI] = self.func_LDI
        self.branchtable[PRN] = self.func_PRN
        self.branchtable[MUL] = self.func_MUL
        self.branchtable[HLT] = self.func_HLT
        self.branchtable[POP] = self.func_POP
        self.branchtable[PUSH] = self.func_PUSH
        self.branchtable[RET] = self.func_RET
        self.branchtable[CALL] = self.func_CALL
        self.branchtable[ADD] = self.func_ADD
        # Store value in registerB in the (this would be self.ram for me )address stored in registerA.
        self.branchtable[ST] = self.func_ST
        self.branchtable[CMP] = self.func_CMP

        self.branchtable[JMP] = self.func_JMP
        self.branchtable[JEQ] = self.func_JEQ
        self.branchtable[JNE] = self.func_JNE        
        

    def load(self):
        """Load a program into memory."""

        """Check to make sure thr right number of arguments were entered"""
        if len(sys.argv) != 2:
            print("Usage: ls8.py --filename")
            sys.exit(1)

        # Sets the address to zero so it can be index when memory is being saved
        address = 0
        # For now, we've just hardcoded a program:
        # program = [
        #     #From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000, # R0 is register 0
        #     0b00001000, # Saving the value of 8
        #     0b01000111, # PRN 
        #     0b00000000, # Printing out R0
        #     HLT, # HLT , Haulting the program
        # ]

        # Allow the command line to run two arguments 
        prog_name = sys.argv[1]
        #
        with open(prog_name) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == '':
                    continue
                # Define the base with 2 since it is binary
                val = int(line, 2)
                print(val)
                self.ram[address] = val
                address += 1
 
        # sys.exit(0)

        # Loops through the program(memory)
        # Gives the address an index and sets it to an instruction
        # for instruction in program:
            # self.ram[address] = val
            #     address += 1

                
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            # if reg_b is less than reg_a
            if self.reg[reg_a] < self.reg[reg_b]:
                # set FL equal to less than
                self.FL = self.FLLT
            # if reg_a is greater_than reg_b
            if self.reg[reg_a] > self.reg[reg_b]:
                # set FL to greater_than
                self.FL = self.FLGT
            # if  registers are equal to
            if self.reg[reg_a] == self.reg[reg_b]:
                # FL is set to equal to 
                self.FL = self.FLET
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    # Helper functions
    # MAR Memory Address Register 
    # Contains Address that is being read
    def ram_read(self, MAR):
        # Memory Address Register 
        return self.ram[MAR]
    # Memory Data Register 
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def func_LDI(self):
        # Saving to register if instruction is LDI
        # saving the value to the register
        # Using the ram_read() helper function  
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)     
        self.reg[operand_a] = operand_b
        # self.pc += 3
    def func_PRN(self):
        # Printing out the register if instruction is PRN
        # Printing out the register and its value
         # Using the ram_read() helper function
        reg_num = self.reg[self.ram_read(self.pc + 1)]
        print(f"Printing register - {reg_num}")
        # self.pc += 2

    def func_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        # self.pc +=3 

    def func_HLT(self):
        #HLT Haulting the pc 
        # self.ram_read(self.pc + 1)
        #Stopping the while Loop
        self.running = False
        print('exit')
    
    def func_POP(self):
        # copy value from the address pointed by SP to given reg
        # increment Stackpointer up
        value = self.ram[self.reg[SP]]
        reg_num = self.ram_read(self.pc +1 )
        self.reg[reg_num] = value 
        self.reg[SP] += 1 

    
    def func_PUSH(self):
        # Decrement SP
        self.reg[SP] -= 1
        # Stack Pointer goes down
        # Copy the value in given register to the address pointed by the SP
        # Gets the register number
        reg_num = self.ram_read(self.pc + 1)
        # Gets the values
        reg_val = self.reg[reg_num]
        self.ram[self.reg[SP]] = reg_val

    def func_CALL(self):
    # CALL 
        # allows for us to return where we left off when subroutine is complete
        return_address = self.pc +2 
        # Decrement SP
        self.reg[SP] -= 1
        # set to address stored in the given register 
        self.ram[self.reg[SP]] = return_address
        # Jump to that location in RAM and execute the first instruction in subroutine 
        # Set the pc to the value in the register 
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]
    # Allows for pc to move forward or backwords from current location

    def func_RET(self):
    # RET 
    # Return from subroutine
        # Pop the return address off the stack
        #store it in the PC
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1

    def func_ADD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("ADD", operand_a, operand_b)

    def func_ST(self):
        # ST
        # Store value in registerB in the address(this would be self.ram for me ) stored in registerA.
        register_A = self.ram[self.pc + 1]
        register_B = self.ram[self.pc + 2]
        # Value in register_B stored into memory in register_a
        self.ram[self.reg[register_A]] = self.reg[register_B]

    def func_CMP(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("CMP", operand_a, operand_b)
        # self.pc += 3

    def func_JMP(self):
        # Jump to the address stored in the given register.
        reg_num = self.ram_read(self.pc + 1)
        # Sets the `PC` to the address stored in the given register.
        self.pc = self.reg[reg_num]
    
    def func_JEQ(self):
        reg_num = self.ram_read(self.pc + 1)
        # If `equal` flag is set (true)
        if self.FL == self.FLET:
             # jump to the address stored in the given register.
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def func_JNE(self):
        reg_num = self.ram_read(self.pc + 1)
        # If `E` flag is clear (false, 0)
        if self.FL != self.FLET:
            # jump to the address stored in the given register.
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2
    
    def run(self):
        """Run the CPU."""
        # Running is set equal to True
        # Loops running 
        while self.running: 
            # Defined short hands
            instruction = self.ram[self.pc]
            # operand_a = self.ram_read(self.pc + 1)
            # operand_b = self.ram_read(self.pc + 2)
            # Moves the IR over 6 places if it the first 2 digits
            op_Count = instruction >> 6
            ir_length = op_Count + 1
            # print(f"ir_length: {ir_length}")
            self.branchtable[instruction]()

            
            if instruction == 0 or None:
                print(f"Not and instruction at {self.pc}")
                sys.exit(1)
            # If the instruction isnt not CALL or RET it will keep the program control going through the stack
            if instruction != CALL and instruction != RET and instruction != JMP and instruction != JEQ and instruction != JNE:
                # print(f"int: {instruction}")
                self.pc += ir_length