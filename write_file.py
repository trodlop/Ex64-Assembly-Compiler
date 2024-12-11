from datetime import datetime

def write_output_file(array):
    with open("output.txt", "w") as file:  # Open file in write mode

        file.write("Ex32 Assembly compiled to 64bit ExC machine code")
        file.write(f"\nCompiled on {datetime.now()}\n\n")

        for item in array:
            file.write(f"{item}\n")  # Write each item followed by a newline

        