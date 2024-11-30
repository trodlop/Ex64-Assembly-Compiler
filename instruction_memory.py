# Reference

#   Instruction layout:

#   Regular Instruction  |  Instruction ID  |  register address  |  register/value  |  register address  |  register address
#   0                    |  0000            |  0000000000000000        |  0               |  0000000000000000        |  0000000000000000

#   NOP.
#   LDI (Load Immediate) r1 value (r2)   ->      0 0001 0000000000000000 0000000000000000 ----------
#   ADD (Add) r1 r2 r3
#   SUB (Subtract) r1 r2 r3
#   MUL r1 r2 r3
#   DIV r1 r2 r3
#   


instruction_list = list()
lines = 0

with open("ROM.txt", "r") as file:
    instruction_list = [
        "" if line.strip().startswith("#") or line.strip() == "" else line.strip()
        for line in file
    ]

# instruction_list = [
#     line.strip() for line in instruction_list
#     if line.strip() and not line.lstrip().startswith("#")
# ]