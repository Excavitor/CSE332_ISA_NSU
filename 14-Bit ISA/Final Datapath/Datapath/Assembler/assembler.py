
                #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
                #                                                           #
                #                         ASSEMBLER                         #
                #                                                           #
                #           Built for a 14-bit ISA based system             #
                #                                                           #
                #  CLI Usage: python assembler.py <input_file> <outputfile> #
                #                                                           #
                #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

import sys

# Key-Value pair Dictionaries to incorporate OPCODE with instructions

# Followed by 3 registers
R_TYPE = {
    "AND": "00000",
    "OR": "00001",
    "NAND": "00010",
    "NOR": "00011",
    "XOR": "00100",
    "ADD": "00111",
    "SUB": "01000",
    "SLT": "01110",
}
# Followed by 2 registers
I_TYPE = {
    "SLL": "00101",
    "SRL": "00110",
    "ADDI": "01001",
    "LW": "01010",
    "SW": "01011",
    "BEQ": "01100",
    "BNE": "01101",
    "SLTI": "01111"
}

# Followed by 1 register
R_TYPE_SHORT = {
    "DIN": "10001",
    "DOUT": "10010"
}


J_TYPE = {
    "JUMP": "10000"
}

# Binary numbers assigned to each register
REGISTERS = {
    "$ZERO": "000",
    "$SP": "001",
    "$S0": "010",
    "$S1": "011",
    "$S2": "100",
    "$S3": "101",
    "$T0": "110",
    "$T1": "111",
}


def convert_to_machine_code(asm_line):

    # To make ASM code case insensetive
    asm_line = asm_line.upper()

    # To remove leading and ending whitespaces
    asm_line = asm_line.strip()

    # Replace all comma with space as space will be the separator of the tokens
    asm_line = asm_line.replace(',', ' ')

    # Create tokens based on spaces
    asm_tokens = asm_line.split() 

    # Output of this function
    machine_code_line = ""

    opcode = asm_tokens[0]

    if opcode in R_TYPE:
        if len(asm_tokens) == 4:
            # When the value of size is given
            _, rd, rs, rt = asm_tokens

            if rd == "$ZERO":
                raise ValueError("$ZERO register can't be modified.")

            if '$' not in rd or '$' not in rs or '$' not in rt:
                raise ValueError("Syntax error.")

            machine_code_line = R_TYPE[opcode] + REGISTERS[rd] + REGISTERS[rs] + REGISTERS[rt]
        else:
            raise ValueError("R type instructions must have 4 tokens.")

    elif opcode in R_TYPE_SHORT:
        if len(asm_tokens) == 2:
            rd = asm_tokens[1]

            if rd == "$ZERO":
                raise ValueError("$ZERO register can't be modified.")

            if '$' not in rd:
                raise ValueError("Syntax error.")

            rs = "$ZERO"
            rt = "$ZERO"
            machine_code_line = R_TYPE_SHORT[opcode] + REGISTERS[rd] + REGISTERS[rs] + REGISTERS[rt]
        else:
            raise ValueError("R-short type instructions must have 2 tokens.")

    elif opcode in I_TYPE:
        if len(asm_tokens) == 4:
            # When the value of size is given
            rd = asm_tokens[1]
            rs = asm_tokens[2]

            if(int(asm_tokens[3]) > 7):
                raise ValueError("Immediate value can't be larger than 7.")

            if(int(asm_tokens[3]) < 0):
                raise ValueError("Immediate value can't be negative")

            if '$' not in rd or '$' not in rs:
                raise ValueError("Syntax error.")

            immediate = format(int(asm_tokens[3]), "03b")

            if rd == "$ZERO":
                raise ValueError("$ZERO register can't be modified.")

            machine_code_line = I_TYPE[opcode] + REGISTERS[rd] + REGISTERS[rs] + immediate
        else:
            raise ValueError("I type instructions must have 4 tokens.")

    elif opcode in J_TYPE:
        if len(asm_tokens) == 2:

            if(int(asm_tokens[1]) > 511):
                raise ValueError("Address value can't be larger than 511.")
            if(int(asm_tokens[1]) < 0):
                raise ValueError("Address value can't be negative")

            address = format(int(asm_tokens[1]), "09b")
            machine_code_line = J_TYPE[opcode] + address
        else:
            raise ValueError("J type instructions must have 2 tokens.")

    else:
        raise ValueError("The opcode was not recognized.")
    # Returns a string machine code
    return machine_code_line 


if __name__ == "__main__":

    # The input and output file name, will be given as terminal arguments
    input_file = open(sys.argv[1], 'r')
    output_file = open(sys.argv[2], 'w')

    # List of Strings
    assembly_code = input_file.readlines()

    # Outputs
    binary_code = []
    hex_code = []

    line_number = 1
    for line in assembly_code:

        # To remove all comments from ASM code line
        line = line.split(';', 1)[0]

        # If line is not empty or whitespace
        if not (line.isspace() or len(line) == 0):

            try:
                machine_code_line = convert_to_machine_code(line)
            except ValueError as er:
                print("Error in Line", line_number, ":", er)
                break

            # Machine code is converted to hex code
            hex_code_line = format(int(machine_code_line, 2), "04X")

            binary_code.append(machine_code_line + '\n')
            hex_code.append(hex_code_line + '\n')
            # machine_code.append(machine_code_line + '\n')

        line_number += 1
    if hex_code:
        print(hex_code)

    output_file.writelines(hex_code)

    binary_file = open("binary.txt", "w")
    binary_file.writelines(binary_code)
    binary_file.close()

    input_file.close()
    output_file.close()
