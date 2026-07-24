import os
import sys
from enum import IntEnum
import subprocess

import tools.other_tools as other_tools

class CompilationFlags(IntEnum):
    EXIT = 0

    RELEASE = 1
    DEBUG = 2

    RELEASE_BUILD = 3
    DEBUG_BUILD = 4

    RELEASE_CLEAR = 5
    DEBUG_CLEAR = 6

def tool_flag_parser(flag: int):
    match flag:
        case CompilationFlags.EXIT:
            print("Exiting program")
            sys.exit(0)
            
        case CompilationFlags.RELEASE | CompilationFlags.DEBUG:
            mode = "release" if flag == CompilationFlags.RELEASE else "debug"
            os_type: str = other_tools.get_os_type()
            
            match os_type:
                case "windows":
                    library_name = "solemp_core.dll"
                case "linux":
                    library_name = "libsolemp_core.so"
                case "macos" | "macos_arm":
                    library_name = "libsolemp_core.dylib"
                case _:
                    print(f"Unknown OS type: {os_type}")
                    return

            old_path = f"solemp-core/target/{mode}/{library_name}"
            new_path = f"solemp-godot/bin/{mode}/{library_name}"
            _move_file(old_path, new_path)

        case CompilationFlags.RELEASE_BUILD:
            _build_cargo("release")
        case CompilationFlags.DEBUG_BUILD:
            _build_cargo("debug")

        case CompilationFlags.RELEASE_CLEAR:
            _clear_cargo("release")
        case CompilationFlags.DEBUG_CLEAR:
            _clear_cargo("debug")

        case _:
            print("Unimplemented flag")
            return

def _build_cargo(flag: str):
    # Start building with command in solemp-core directory
    # Resolve project root path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    cargo_dir = os.path.join(project_root, "solemp-core")

    # Start build or release command depend on flag 
    command = ["cargo", "build"]
    if flag == "release":
        command.append("--release")

    print(f"Running {' '.join(command)} in {cargo_dir}...")

    try:
        # Execute cargo build inside the solemp-core subdirectory
        subprocess.run(command, cwd=cargo_dir, check=True)
        print("Cargo build finished successfully!") 
    except subprocess.CalledProcessError:
        print("Error: Cargo build failed!")
    except FileNotFoundError:
        print("Error: 'cargo' command not found. Cheak Rust intstallation")

def _clear_cargo(flag: str):
    # Start building with command in solemp-core directory
    # Resolve project root path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    cargo_dir = os.path.join(project_root, "solemp-core")

    # Start build or release command depend on flag 
    command = ["cargo", "clean"]
    if flag == "release":
        command.append("--release")
    elif flag == "debug":
        # Target dev profile artifacts specifically for clean command
        command.append("--profile")
        command.append("dev")

    print(f"Running {' '.join(command)} in {cargo_dir}...")

    try:
        # Execute cargo clean inside the solemp-core subdirectory
        subprocess.run(command, cwd=cargo_dir, check=True)
        print("Cargo clear finished successfully!") 
    except subprocess.CalledProcessError:
        print("Error: Cargo clear failed!")
    except FileNotFoundError:
        print("Error: 'cargo' command not found. Cheak Rust intstallation")

def _move_file(old_path, new_path):
    # Moving files from old path to new path
    try:
        # Create missing nested folders in target path before moving file
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        
        if os.path.exists(new_path):
            user_choice_bool: bool = True
            while user_choice_bool:
                user_choice = input(f"File '{new_path}' already exists. Overwrite? (y|N): ").lower().strip()
                user_choice_bool = False
                match user_choice:
                    case 'y':
                        os.remove(new_path)
                        print(f"Previos file '{new_path}' was deleted")

                    case 'n' | '':
                        print("File overwriting canceled")
                        return

                    case _:
                        print("Unknown input. Please enter 'y' or 'n'")
                        user_choice_bool = True

        os.rename(old_path, new_path)
        print(f"File successful moved. From -> {old_path} to {new_path}")
    except FileNotFoundError:
        print(f"File -> {old_path} not found")
    except PermissionError:
        print("No access rights")
