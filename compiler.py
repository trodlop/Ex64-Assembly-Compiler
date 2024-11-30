import instruction_memory as inst

final_instructions = list()

op_codes = {
        "NOP" : "00000",
        "LDI" : "00001",
        "MVE" : "00010",
        "ADD" : "00011",
        "SUB" : "00100",
        "MUL" : "00101",
        "DIV" : "00110",
        "SCF" : "00111",
        "COMP>" : "01000",
        "COMP<" : "01001",
        "COMP=" : "01010",
        "COMP!=" : "01011",

        "HLT" : "11111"
    }

number_type = inst.instruction_list[0][-2:]

def check_valid_register(register, instruction, i):

    if register[0] == "@": # Checks if the register address is correctly syntaxed

        register = register[1:]

        if number_type == "0x": # Checks for valid denary register address

            try: # Checks for invalid integer 
                int(register)
            except ValueError:
                exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, register address must be a valid integer")

            if int(register) == 0: # Checks if trying to access 0th register
                exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, cpu does not allow referencing of the 0th register")

            elif int(register) > 255 or int(register) < 0: # Checks if register address is out of bounds
                exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, register address is out of bounds (address must be between 1 and 255)")

            else: # Decimal register address is valid
                return

        elif number_type == "0b": # Checks for a valid 8bit binary number

            if len(register) == 8 and all(c in '01' for c in register): # Binary register address is valid
                return

            else: # Binary register address is invalid
                exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, register address must be a valid 8bit binary number")

    else: # Error for incorrectly syntaxed register address
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, must be a register address (register addresses begin with '@')")

def check_valid_value(value, instruction, i):

    if value == "@": # Check if immediate value syntaxed as register
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, immediate value syntaxed as register address (immediate values do not start with '@')")

    elif number_type == "0x": # Checks if the immediate value is valid integer

        try:
            int(value)
        except ValueError:
            exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, immediate value must be a valid integer")

        if int(value) > 65535 or int(value) < 0: # Checks if register address is out of bounds
            exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, immediate value is out of bounds (value must be between 0 and 65535)")

        else: # Decimal register address is valid
            return

    elif number_type == "0b": # Checks if the immediate value is valid 16bit binary number

        if value != 16 and all(c in '01' for c in value): # Binary register address is valid
            return

        else: # Binary register address is invalid
            exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{instruction[1]}, immediate value must be a valid 16bit binary number")


def compile_NOP(assembly_instruction, i):

    if len(assembly_instruction) > 1: # Checks if NOP is incorrectly syntaxed
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction[1:]}, NOP instructions must not be followed by any values")

    else: # NOP is correctly syntaxed
        machine_instruction = "0" * 64 # NOP instructions are just all 0s

        final_instructions.append(machine_instruction) # Adds the finished machine code instruction to final instruction list

def compile_LDI(assembly_instruction, i):

    machine_instruction = ""

    machine_instruction += op_codes[f"{assembly_instruction[0]}"] # Converts the opcode to machine code and adds it to the machine code instruction

    check_valid_register(assembly_instruction[1], assembly_instruction, i) # Checks that the register address is valid

    if number_type == "0b": # Checks if the number type is binary
        address = assembly_instruction[1][1:] # Retrieves the 8bit address

    elif number_type == "0x": # Checks if the number type is decimal
        address = bin(int(assembly_instruction[1][1:]))[2:].zfill(8) # Converts the denary address to an 8bit binary number

    machine_instruction += "1" # Adds register address flag to machine code instruction
    machine_instruction += "00000000" # Adds 8bits to the front of the address to maintain instruction length
    machine_instruction += f"{address}" # Adds the 8bit register to machine code instruction

    check_valid_value(assembly_instruction[2], assembly_instruction, i) # Checks that the immediate value is valid

    if number_type == "0b": # Checks if the number type is binary
        value = assembly_instruction[2] # Retrieves the 16bit value

    elif number_type == "0x": # Checks if the number type is decimal
        value = bin(int(assembly_instruction[2]))[2:].zfill(16) # Converts the denary address to an 16bit binary number

    machine_instruction += "0" # Adds immediate value flag to machine code instruction
    machine_instruction += f"{value}" # Adds 16bit value to machine code instruction

    machine_instruction += "000000000000000000000000" # Adds remaining bits to keep instruction at 64bits

    if len(assembly_instruction) > 3 and assembly_instruction[3] != "CONDITIONAL": # Checks for syntax error in CONDITIONAL instruction
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

    elif len(assembly_instruction) > 3 and assembly_instruction[3] == "CONDITIONAL":
        machine_instruction += "1"
        add_to_final_instruction_list(machine_instruction)

    elif len(assembly_instruction) == 3:
        machine_instruction += "0"
        add_to_final_instruction_list(machine_instruction)

    else:
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

def compile_MVE(assembly_instruction, i):

    machine_instruction = ""

    machine_instruction += op_codes[f"{assembly_instruction[0]}"] # Converts the opcode to machine code and adds it to the machine code instruction

    check_valid_register(assembly_instruction[1], assembly_instruction, i) # Checks that the register address is valid

    if number_type == "0b": # Checks if the number type is binary
        address = assembly_instruction[1][1:] # Retrieves the 8bit address

    elif number_type == "0x": # Checks if the number type is decimal
        address = bin(int(assembly_instruction[1][1:]))[2:].zfill(8) # Converts the denary address to an 8bit binary number

    machine_instruction += "1" # Adds register address flag to machine code instruction
    machine_instruction += "00000000" # Adds 8bits to the front of the address to maintain instruction length
    machine_instruction += f"{address}" # Adds the 8bit register to machine code instruction

    check_valid_register(assembly_instruction[2], assembly_instruction, i) # Checks that the immediate value is valid

    if number_type == "0b": # Checks if the number type is binary
        address = assembly_instruction[2] # Retrieves the 16bit value

    elif number_type == "0x": # Checks if the number type is decimal
        address = bin(int(assembly_instruction[2][1:]))[2:].zfill(8) # Converts the denary address to an 16bit binary number

    machine_instruction += "1" # Adds register address flag to machine code instruction
    machine_instruction += "00000000" # Adds 8bits to the front of the address to maintain instruction length
    machine_instruction += f"{address}" # Adds the 8bit register to machine code instruction

    machine_instruction += "000000000000000000000000" # Adds remaining bits to keep instruction at 64bits

    if len(assembly_instruction) > 3 and assembly_instruction[3] != "CONDITIONAL": # Checks for syntax error in CONDITIONAL instruction
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

    elif len(assembly_instruction) > 3 and assembly_instruction[3] == "CONDITIONAL":
        machine_instruction += "1"
        add_to_final_instruction_list(machine_instruction)

    elif len(assembly_instruction) == 3:
        machine_instruction += "0"
        add_to_final_instruction_list(machine_instruction)

    else:
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")


def compile_CLR(assembly_instruction, i):

    if assembly_instruction[-1] == "CONDITIONAL":
        compile_LDI(["LDI", assembly_instruction[1], "0", assembly_instruction[-1]], i)
    elif len(assembly_instruction) == 2:
        compile_LDI(["LDI", assembly_instruction[1], "0"], i)
    else:
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

def compile_arithmetic(assembly_instruction, i):

    machine_instruction = ""

    machine_instruction += op_codes[f"{assembly_instruction[0]}"] # Converts the opcode to machine code and adds it to the machine code instruction

    for j in range(2):

        if assembly_instruction[j+1][0] == "@":
            check_valid_register(assembly_instruction[j+1], assembly_instruction, j) # Checks that the register address is valid

            if number_type == "0b": # Checks if the number type is binary
                address = assembly_instruction[j+1][1:] # Retrieves the 8bit address

            elif number_type == "0x": # Checks if the number type is decimal
                address = bin(int(assembly_instruction[j+1][1:]))[2:].zfill(8) # Converts the denary address to an 8bit binary number

            machine_instruction += "1" # Adds register address flag to machine code instruction
            machine_instruction += "00000000" # Adds 8bits to the front of the address to maintain instruction length
            machine_instruction += f"{address}" # Adds the 8bit register to machine code instruction

        else:
            check_valid_value(assembly_instruction[j+1], assembly_instruction, j) # Checks that the immediate value is valid

            if number_type == "0b": # Checks if the number type is binary
                value = assembly_instruction[1] # Retrieves the 16bit value

            elif number_type == "0x": # Checks if the number type is decimal
                value = bin(int(assembly_instruction[j+1]))[2:].zfill(16) # Converts the denary address to an 16bit binary number

            machine_instruction += "0" # Adds immediate value flag to machine code instruction
            machine_instruction += f"{value}" # Adds 16bit value to machine code instruction

    check_valid_register(assembly_instruction[3], assembly_instruction, i) # Checks that the register address is valid

    if number_type == "0b": # Checks if the number type is binary
        address = assembly_instruction[3][1:] # Retrieves the 8bit address

    elif number_type == "0x": # Checks if the number type is decimal
        address = bin(int(assembly_instruction[3][1:]))[2:].zfill(8) # Converts the denary address to an 8bit binary number

    machine_instruction += "1" # Adds register address flag to machine code instruction
    machine_instruction += "00000000" # Adds 8bits to the front of the address to maintain instruction length
    machine_instruction += f"{address}" # Adds the 8bit register to machine code instruction

    machine_instruction += "0000000" # Adds remaining bits to keep instruction at 64bits

    if len(assembly_instruction) > 4 and assembly_instruction[4] != "CONDITIONAL": # Checks for syntax error in CONDITIONAL instruction
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

    elif len(assembly_instruction) > 4 and assembly_instruction[4] == "CONDITIONAL":
        machine_instruction += "1"
        add_to_final_instruction_list(machine_instruction)

    elif len(assembly_instruction) == 4:
        machine_instruction += "0"
        add_to_final_instruction_list(machine_instruction)

    else:
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

def compile_SCF(assembly_instruction, i):
    
    machine_instruction = ""

    machine_instruction += op_codes[f"{assembly_instruction[0]}"] # Converts the opcode to machine code and adds it to the machine code instruction

    machine_instruction += "0" *57

    if len(assembly_instruction) == 2:

        if assembly_instruction[1] != "1" and assembly_instruction[1] != "0":
            exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction[1]}, conditional flag must either be 0 (for false), or 1 (for true)")
        else:
            machine_instruction += f"{assembly_instruction[1]}0"

    elif len(assembly_instruction) == 3 and assembly_instruction[2] == "CONDITIONAL":

        if assembly_instruction[1] != "1" and assembly_instruction[1] != "0":
            exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction[1]}, conditional flag must either be 0 (for false), or 1 (for true)")
        else:
            machine_instruction += f"{assembly_instruction[1]}1"

    else:
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

    add_to_final_instruction_list(machine_instruction)
            

def compile_COMP_greater(assembly_instruction, i):
    print("compiled COMP> instruction")   

def compile_COMP_less(assembly_instruction, i):
    print("compiled COMP< instruction")   

def compile_COMP_equal(assembly_instruction, i):
    print("compiled COMP= instruction")   

def compile_COMP_nequal(assembly_instruction, i):
    print("compiled COMP!= instruction")   

def compile_HLT(assembly_instruction, i):
    
    machine_instruction = ""

    machine_instruction += op_codes[f"{assembly_instruction[0]}"] # Converts the opcode to machine code and adds it to the machine code instruction

    machine_instruction += "0" *58

    if len(assembly_instruction) == 1:
        machine_instruction += "0"

    elif len(assembly_instruction) == 2 and assembly_instruction[1] == "CONDITIONAL":
        machine_instruction += "1"

    else:
        exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction}, syntax error")

    add_to_final_instruction_list(machine_instruction)

def add_to_final_instruction_list(instruction):
    final_instructions.append(instruction) # Adds the passed finished machine code instruction to final instruction list

def begin_compile():

    if number_type != "0b" and number_type != "0x": # Checks is the number type passed is not valid (0b or 0x)
        exit(f"Error in compiling, line 0 - in {inst.instruction_list[0]},\n{inst.instruction_list[0]}, number type must either be 0x or 0b")

    if inst.instruction_list[0] != "NUMTYPE = 0b" and inst.instruction_list[0] != "NUMTYPE = 0x": # Checks if the syntax is valid
        exit(f"Error in compiling, line 0 - in {inst.instruction_list[0]},\n{inst.instruction_list[0]}, invalid syntax")
    
    inst.instruction_list[0] = ""

    for i in range(len(inst.instruction_list)):

        if inst.instruction_list[i] == "": # If line is empty 
            continue

        assembly_instruction = inst.instruction_list[i].split(" ") # Returns an array

        if assembly_instruction[0] == "NOP":
            compile_NOP(assembly_instruction, i)

        elif assembly_instruction[0] == "LDI":
            compile_LDI(assembly_instruction, i)

        elif assembly_instruction[0] == "MVE":
            compile_MVE(assembly_instruction, i)

        elif assembly_instruction[0] == "CLR":
            compile_CLR(assembly_instruction, i)

        elif assembly_instruction[0] == "ADD":
            compile_arithmetic(assembly_instruction, i)

        elif assembly_instruction[0] == "SUB":
            compile_arithmetic(assembly_instruction, i)

        elif assembly_instruction[0] == "MUL":
            compile_arithmetic(assembly_instruction, i)

        elif assembly_instruction[0] == "DIV":
            compile_arithmetic(assembly_instruction, i)

        elif assembly_instruction[0] == "SCF":
            compile_SCF(assembly_instruction, i)


        elif assembly_instruction[0] == "COMP>":
            compile_COMP_greater(assembly_instruction, i)

        elif assembly_instruction[0] == "COMP<":
            compile_COMP_less(assembly_instruction, i)

        elif assembly_instruction[0] == "COMP=":
            compile_COMP_equal(assembly_instruction, i)

        elif assembly_instruction[0] == "COMP!=":
            compile_COMP_nequal(assembly_instruction, i)
        

        elif assembly_instruction[0] == "HLT":
            compile_HLT(assembly_instruction, i)

        else: # Checks for invalid operation code
            exit(f"Error in compiling, line {i + 1} - in {inst.instruction_list[i]},\n{assembly_instruction[0]} is not a valid operation")
    
begin_compile()
print(final_instructions)