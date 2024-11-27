# Reference

#   Instruction layout:

#   Regular Instruction  |  Instruction ID  |  register address  |  register/value  |  register address  |  register address
#   0                    |  0000            |  0000000000000000        |  0               |  0000000000000000        |  0000000000000000

#   NOP.
#   LDI, (Load Immediate) r1, value (r2).   ->      0 0001 0000000000000000 0000000000000000 ----------
#   ADD, (Add) r1, r2, r3.
#   SUB, (Subtract) r1, r2, r3.
#   


instruction_list = list()

with open("ROM.txt", "r") as ROM:
    instruction_list = ROM.readlines()

instruction_list = [line.strip() for line in instruction_list]

print(instruction_list)
