import tools.core_to_godot as core_to_godot
import tools.other_tools as other_tools

TOOLS: list[str] = [
    "Exit", # 0

    "Move release compiled file from solemp-core to solemp-godot", # 1
    "Move debug compiled file from solemp-core to solemp-godot", # 2

    "\n",

    "Compile release sole-mp core", # 3
    "Compile debug sole-mp core" # 4

    "\n",

    "Clear compiled release files solemp-core", # 5
    "Clear compiled debug files solemp-core" # 6
    ]

def _new_line_count() -> int:
    # Count newline formatting elements to calculate valid index ranges
    result: int = 0
    for element in TOOLS:
        if element == "\n":
            result += 1

    return result

def _tools_text():
    print("""\n\n
             _____   ___    ___   _      ____  
            |_   _| / _ \\  / _ \\ | |    / ___| 
              | |  | | | || | | || |    \\___ \\ 
              | |  | |_| || |_| || |___  ___) |
              |_|   \\___/  \\___/ |_____||____/ 
""")
    _new_line_count: int = 0
    for element_num in range(0, len(TOOLS)):
        if element_num != 0:
            if not TOOLS[element_num] == "\n":
                # Shift display indices to ignore formatting newlines
                print(f"{element_num - _new_line_count}. {TOOLS[element_num]}")
            else:
                print("")
                _new_line_count += 1
    print(f"\n0. {TOOLS[0]}\n")

def _access_input(tool_num: int) -> bool:
    # Checking confirmation from user and returning result
    target_tool_text: str = ""
    target_tool_real_id: int = -1
    current_num = 0

    # Map the displayed tool number back to its real index in TOOLS array
    for num, element in enumerate(TOOLS):
        if num != 0 and element != "\n":
            current_num += 1
            if current_num == tool_num:
                target_tool_text = element
                target_tool_real_id = num
                break

    if target_tool_real_id == -1:
        print("Error: tool not found")
        return False

    access_input_work: bool = True
    while access_input_work:
        access_input: str = input(f'\nWARNING:\nContinue "{tool_num}. {target_tool_text}" (y|N) ')
        access_input_work = False
        match access_input.lower():
            case "y":
                return True
            
            case "n" | "": 
                print("Action aborted")
                return False
            
            case _:
                print("Unknown input")
                access_input_work = True

def input_parser():
    # Calling function depend on input result
    other_tools._console_clear_()
    _tools_text()

    user_input_bool = True
    while user_input_bool:
        try:
            user_input = int(input("Enter option number -> "))
            user_input_bool = False
        except ValueError:
            print("Invalid value. Please enter a number.")

    match user_input:
        case 0:
            core_to_godot.tool_flag_parser(0)
            
        # Dynamically check if the number falls into the valid displayed menu range
        case num if 1 <= num <= (len(TOOLS) - _new_line_count() - 1):
            if _access_input(num):
                core_to_godot.tool_flag_parser(num)

        case _:
            print("Unknown flag")


    # Handle post-execution choice: repeat main loop or exit script
    user_input_bool: bool = True
    while user_input_bool:
        try:
            user_input_continue: str = input("\nContinue (Y|n) ")
            match user_input_continue.lower():
                case "n":
                    core_to_godot.tool_flag_parser(0)
                    user_input_bool = False

                case "y" | "":
                    print("")
                    user_input_bool = False

                case _:
                    print("Unknown flag")
        except ValueError:
            print("Invalid value")

def main():
    input_parser()

if __name__ == "__main__":
    while True:
        main()
