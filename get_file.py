instruction_list = list()
lines = 0

file_address = str(input("\n--- Compile Ex32 Assembly file ---\n\nEnter file address:\n./"))

# file_address = "ROM.txt"

with open(file_address, "r") as file:
    try:
        instruction_list = [
            "" if line.strip().startswith("#") or line.strip() == "" else line.strip()
            for line in file
        ]
    except:
        print("File address is not valid")