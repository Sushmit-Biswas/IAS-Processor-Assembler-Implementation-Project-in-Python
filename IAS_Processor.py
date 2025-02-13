# This module simulates the IAS (Institute for Advanced Study) machine.
# The IAS architecture is an early computer design featuring a von Neumann style single storage for instructions and data.
# This assignment implements instruction decoding, execution cycles, and control flow similar to the IAS machine.

# The program is designed to solve a quadratic equation (ax^2 + bx + c = 0) using the IAS machine.
# The coefficients are input by the user and stored in memory locations.
# But it has 2 extra operations: DISC and SQRT

# Run the program and follow the instructions to input the coefficients and view the results.

# Import and installation checks for required modules (colorama and rich)
# Error handling for missing modules
try:
    from colorama import init, Fore, Style
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Style

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    import subprocess, sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.panel import Panel

import os
import IAS_Assembler

# Global setup for console styling and initialization
init()
console = Console()


def clear_screen():
    # Clears terminal screen for better visualization between instruction cycles.
    # Uses OS-specific commands: "cls" for Windows and "clear" for Unix-based systems.
    os.system("cls" if os.name == "nt" else "clear")


def print_box(text, color=Fore.WHITE):
    # Prints text within a styled box on the terminal.
    # This helps in highlighting key messages on the IAS machine display.
    width = 60
    print(f"{color}╔{'═' * (width-2)}╗")
    print(f"║{text.center(width-2)}║")
    print(f"╚{'═' * (width-2)}╝{Style.RESET_ALL}")


def print_register_state():
    # Displays the current state of key IAS registers.
    # Registers shown: Program Counter (PC), Accumulator (AC), and Multiplier Quotient (MQ).
    # This provides insight into the execution state after each machine instruction.
    print(f"{Fore.CYAN}{'-'*40}")
    print(f"{'Register':10s} | {'Value':>10s}")
    print(f"{'-'*40}")
    print(f"{'PC':10s} | {PC:10}")
    print(f"{'AC':10s} | {AC:10}")
    print(f"{'MQ':10s} | {MQ:10}")
    print(f"{'-'*40}{Style.RESET_ALL}\n")


def print_final_result(message):
    # Uses the rich module to present final results in a stylized panel.
    # This encapsulates the outcome of the quadratic equation solver.
    panel = Panel(
        message, title="RESULTS", title_align="center", style="bright_magenta"
    )
    console.print(panel)

# Global registers and memory initialization
# The registers include: MAR (Memory Address Register), IR (Instruction Register),
# PC (Program Counter), IBR (Instruction Buffer Register), AC (Accumulator), MQ (Multiplier-Quotient Register) and MBR (Memory Buffer Register).
# The memory M simulates storage where data (equation coefficients) and instructions are loaded.
MAR = ""
IR = ""
PC = 0
IBR = ""
AC = 0
MQ = 0
MBR = 0

# Initialize memory locations
a, b, c, a_2, dis, root_d, x1, x2 = 0, 0, 0, 0, 0, 0, 0, 0
M = [a, b, c, a_2, dis, 4, 2, root_d, x1, x2]
# equation: ax^2 + bx + c
# a_2 stores the value of 2a needed for denominator
# dis stores the value of discriminant
# x1 and x2 are the roots


def my_operation(op, address):
    # Core function to simulate the execution of a machine-level instruction.
    # Each instruction is defined by its opcode and memory address operand.
    # Additional operations DISC (for discriminant calculation) and SQRT (for square root extraction) are implemented.
    global PC
    global MAR
    global IR
    global IBR
    global MBR
    global AC
    global MQ

    # op is the opcode and address is the memory address
    # Added 2 new operations: DISC and SQRT
    if op == "01010101":  # DISC M[x],M[x],M[x]
        # Computes the discriminant for a quadratic equation: (b^2 - 4ac).
        # The 'address' string encodes indices for a, b, and c in memory.
        bin_a = address[0:4]
        bin_b = address[4:8]
        bin_c = address[8:12]
        a = M[int(bin_a, 2)]
        b = M[int(bin_b, 2)]
        c = M[int(bin_c, 2)]
        discriminant = (b**2) - (4 * a * c)
        AC = discriminant
    
    elif op == "00110011":  # SQRT M[x]
        # Retrieves a value from memory and computes its square root.
        # This operation may be used to calculate the final roots of the quadratic equation.
        MBR = M[int(address, 2)]
        AC = MBR
        AC = AC**0.5

    elif op == "00000010":  # LOAD -M[x]
        # Loads a memory value, negates it, and stores it in the accumulator.
        MBR = M[int(address, 2)]
        AC = -MBR
    elif op == "00100001":  # STOR M[x]
        # Stores the current value of the accumulator into the memory at the given address.
        MBR = AC
        M[int(address, 2)] = MBR
    elif op == "00001101":  # JUMP M(X,0:19)
        # Take next instruction from left half of M(X)
        PC = int(address, 2) - 1
    elif op == "00001111":  # JUMP+ M[x,0:19]
        # Jumps to a different memory address if the accumulator is non-negative.
        if AC >= 0:
            PC = int(address, 2) - 1
    elif op == "00000101":  # ADD M[x]
        # Adds the memory value at the specified address to the current accumulator value.
        MBR = M[int(address, 2)]
        AC = AC + MBR
    elif op == "00000110":  # SUB M[x]
        # Subtracts the memory value at the given address from the accumulator.
        MBR = M[int(address, 2)]
        AC = AC - MBR
    elif op == "00001100":  # DIV M[x]
        # Divides the accumulator value by the memory value.
        # Stores the quotient in MQ and remainder in AC.
        MBR = M[int(address, 2)]
        MQ = AC / MBR
        AC = AC % MBR
    elif op == "00001011":  # MUL M[x]
        # Executes multiplication utilising MQ.
        # The memory value is loaded into MBR, then multiplied with MQ.
        MBR = M[int(address, 2)]
        AC = MBR
        MQ = AC * MQ
    elif op == "00001001":  # LOAD MQ,M[x]
        # Loads a memory value into the MQ register.
        MBR = M[int(address, 2)]
        MQ = MBR
    elif op == "00001010":  # LOAD MQ
        # Transfers the value from the MQ register into the accumulator.
        AC = MQ
    elif op == "00000010":  # LOAD -M[x]
        # Duplicate case: Loads and negates the memory value.
        AC = -M[int(address, 2)]


def decode_instruction(word):  # word is a string , stored at M[PC]
    # Decodes a 40-bit instruction word into two 20-bit instructions.
    # Each 20-bit instruction comprises an 8-bit opcode and a 12-bit address field.
    # The left instruction is executed first, followed by the right if present.
    global PC
    global MAR
    global IR
    global IBR
    global MBR
    global AC
    global MQ

    # Assume PC set to address of instrucion
    MAR = str(PC)

    MBR = word  # First the word goes to MBR from M[MAR]

    # Transfer the word present in the MBR
    left_instruction = MBR[0:20]
    left_opcode = MBR[0:8]
    left_address = MBR[8:20]
    right_instruction = MBR[20:40]
    right_opcode = MBR[20:28]
    right_address = MBR[28:40]

    # Execute left instruction: update IR and MAR accordingly.
    IR = left_opcode  # From MBR , left address opcode goes to IR
    MAR = left_address  # from MBR , left address goes to MAR
    IBR = right_instruction  # from MBR, right instruction goes to IBR

    my_operation(IR, MAR)  # Execute left instruction

    # Now decode and execute right instruction from the IBR.
    IR = IBR[0:8]  # from IBR , load right opcode in IR
    MAR = IBR[8:20]  # from IBR , load right address in MAR

    my_operation(IR, MAR)  # Execute right instruction

    # Increment PC to point to the next instruction word.
    PC = int(PC) + 1  # increment PC to point to next word's memory location


# Main program execution starts here.
clear_screen()
print_box("IAS Machine Quadratic Equation Solver", Fore.GREEN)
print_box("ax² + bx + c = 0", Fore.CYAN)

# Prompt user input for quadratic coefficients with range validation.
print(f"{Fore.YELLOW}Enter co-efficients (-15 ≤ a, b, c ≤ 15 AND a ≠ 0):{Style.RESET_ALL}")
a_in = int(input(f"{Fore.GREEN}a: {Style.RESET_ALL}"))
b_in = int(input(f"{Fore.GREEN}b: {Style.RESET_ALL}"))
c_in = int(input(f"{Fore.GREEN}c: {Style.RESET_ALL}"))

# Store the coefficients in the designated memory locations.
M[0] = a_in
M[1] = b_in
M[2] = c_in

# Set PC to the starting address for the instruction sequence.
PC = 496
i = 0  # Instruction index for the machine language program.
mach_lang = []
mach_lang = IAS_Assembler.mach_lang_prog(mach_lang)

# Execute instructions until either HALT is signaled or the PC reaches termination conditions.
while True:
    if PC == 510:
        break
    if mach_lang[i] == "00000000000000000000000000000000000000000" or PC == 499:  # HALT condition.
        break

    decode_instruction(mach_lang[i])
    print_register_state()  # Visualize register changes after each cycle.
    i += 1

# After completing instruction execution, determine and display the result.
if PC == 499:
    result_str = "No real roots exist since the discriminant is negative."
else:
    result_str = f"The roots are {M[8]} and {M[9]}"
print_final_result(result_str)
