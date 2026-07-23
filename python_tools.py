import tools.core_to_godot as core_to_godot

def _tools_text():
    print("""\n\n
             _____   ___    ___   _      ____  
            |_   _| / _ \\  / _ \\ | |    / ___| 
              | |  | | | || | | || |    \\___ \\ 
              | |  | |_| || |_| || |___  ___) |
              |_|   \\___/  \\___/ |_____||____/ 

1. Move realese compiled file from solemp-core to solemp-godot
2. Move debug compiled file from solemp-core to solemp-godot

3. Compile realese sole-mp core
4. Compile debug sole-mp core

0. Exit
""")

def _access_input() -> bool:
    access_input_work: bool = True
    while access_input_work:
        access_input: str = input("WARNING: Continue(y|N)")
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
    _tools_text()
    user_input: int = int(input())

    match user_input:
        case 0:
            core_to_godot.tool_flag_parser(0)
            
        case num if 1 <= num <= 4:
            if _access_input():
                core_to_godot.tool_flag_parser(num)

        case _:
            print("Unknown flag")

def main():
    input_parser()

if __name__ == "__main__":
    while True:
        main()