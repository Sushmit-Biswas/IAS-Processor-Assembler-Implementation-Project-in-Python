# This module contains the functions to convert IAS assembly code to machine language.

import sys
from colorama import init, Fore, Style

init()  # Initialize colorama for colored terminal output

# Opcode dictionary mapping each assembly mnemonic to its binary opcode
OPCODES = {
    "LOAD -M(X)": "00000010",
    "LOAD MQ,M(X)": "00001001",
    "LOAD MQ": "00001010",
    "DISC M(X),M(X),M(X)": "01010101",
    "JUMP+ M(X,0:19)": "00001111",
    "SQRT M(X)": "00110011",
    "STOR M(X)": "00100001",
    "MUL M(X)": "00001011",
    "SUB M(X)": "00000110",
    "ADD M(X)": "00000101",
    "DIV M(X)": "00001100",
    "HALT": "00000000",
}

# Returns the binary opcode corresponding to the instruction string.
def opcode(instruction):
    return OPCODES.get(instruction, None)

# Converts a decimal operand into a fixed-width binary string.
# DISC instructions use 4-bit formatting; others use 12-bit.
def convert_binary(x, my_opcode):
    x = int(x)
    return bin(x)[2:].zfill(4 if my_opcode == "01010101" else 12)

# Print machine language program
def print_machine_lang_program(mach_lang, color=Fore.YELLOW):
    width = 80
    # Print header box
    print(f"{color}╔{'═' * (width-2)}╗")
    header = "Machine Language Program"
    print(f"║{header.center(width-2)}║")
    print(f"╠{'═'*(width-2)}╣")
    # Print each instruction on a new line
    for inst in mach_lang:
        print(f"║{inst.ljust(width-2)}║")
    print(f"╚{'═'*(width-2)}╝{Style.RESET_ALL}\n")

# Main function to build and output the machine language program
def mach_lang_prog(mach_lang):
    print("\nPlease type the IAS commands:\n")
    zeroes = "00000000000000000000"  # Padding to complete the instruction length
    while True:
        ins_list = input("").split()
        if ins_list[0] == "EXIT":  # Terminates input when user types EXIT.
            break
        else:
            # For JUMP+ commands (example: JUMP+ M(500,0:19))
            if ins_list[0] == "JUMP+":
                op = opcode("JUMP+ M(X,0:19)")
                # Extract operand between '(' and ',' e.g. from M(500,0:19)
                operand = ins_list[1][ ins_list[1].find('(')+1 : ins_list[1].find(',') ]
                binary = convert_binary(operand, op)
                address = op + binary + zeroes

            # For single part instructions
            elif len(ins_list) == 2:
                if ins_list[0] == "DISC":
                    # Use complete mnemonic from dictionary
                    op = opcode("DISC M(X),M(X),M(X)")
                    # Extract each operand digit from a string like "M(0),M(1),M(2)"
                    mem_a = ins_list[1][2]           # '0' from "M(0)"
                    mem_b = ins_list[1][7]           # '1' from "M(1)"
                    mem_c = ins_list[1][12]          # '2' from "M(2)"
                    binary = (convert_binary(mem_a, op)
                              + convert_binary(mem_b, op)
                              + convert_binary(mem_c, op))
                    address = op + binary + zeroes
                elif ins_list[0] == "LOAD" and ins_list[1].startswith("MQ,M"):
                    op = opcode("LOAD MQ,M(X)")
                    # For "MQ,M(0)" extract digit at index 5: M, Q, ',', M, '(', digit, ')'
                    binary = convert_binary(ins_list[1][5], op)
                    address = op + binary + zeroes
                elif ins_list[0] == "LOAD" and ins_list[1].startswith("MQ"):
                    op = opcode("LOAD MQ")
                    # Here we assume a dummy operand if none provided
                    binary = convert_binary(ins_list[1][6] if len(ins_list[1]) > 6 else 0, op)
                    address = op + binary + zeroes
                else:
                    # For instructions like STOR, ADD, SUB, MUL, DIV using format "INST M(x)"
                    op = opcode(ins_list[0] + " M(X)")
                    # Extract the memory index from string like "M(4)"
                    binary = convert_binary(ins_list[1][2], op)
                    address = op + binary + zeroes

            # For instructions with 4 parts (composite instructions)
            elif len(ins_list) == 4:
                if ins_list[1][0] == "-":
                    # Process negative load: e.g. LOAD -M(1)
                    op = opcode("LOAD -M(X)")
                    binary = convert_binary(ins_list[1][3], op)
                    address = op + binary
                    # Process the second instruction; e.g., ADD M(7)
                    op_part2 = opcode(ins_list[2] + " M(X)")
                    binary = convert_binary(ins_list[3][2], op_part2)
                    address = address + op_part2 + binary
                elif ins_list[2] == "LOAD" and ins_list[3] == "MQ":
                    # Process composite instructions like: MUL M(6) LOAD MQ
                    op = opcode(ins_list[0] + " M(X)")
                    binary = convert_binary(ins_list[1][2], op)
                    address = op + binary
                    op2 = opcode("LOAD MQ")
                    binary = "000000000000"  # Fixed binary string for LOAD MQ
                    address = address + op2 + binary
                elif ins_list[1][1] == "-":
                    op = opcode("LOAD -M(X)")
                    binary = convert_binary(ins_list[1][3], op)
                    address = op + binary
                    op2 = opcode(ins_list[2] + " M(X)")
                    binary = convert_binary(ins_list[3][2], op2)
                    address = address + op2 + binary
                else:
                    # Process two-part instructions (e.g. ADD then SUB)
                    op = opcode(ins_list[0] + " M(X)")
                    binary = convert_binary(ins_list[1][2], op)
                    address = op + binary
                    op2 = opcode(ins_list[2] + " M(X)")
                    binary = convert_binary(ins_list[3][2], op2)
                    address = address + op2 + binary
        mach_lang.append(address)
        
    # Output the machine language program in a neat, colored box.
    print_machine_lang_program(mach_lang)
    return mach_lang