import os
import sys
from enum import IntEnum
import subprocess

class CompilationFlags(IntEnum):
    EXIT = 0
    RELEASE = 1
    DEBUG = 2
    RELEASE_BUILD = 3
    DEBUG_BUILD = 4

def tool_flag_parser(flag: int):
    match flag:
        case CompilationFlags.EXIT:
            print("Exiting program")
            sys.exit(0)
            
        case CompilationFlags.RELEASE:
            old_path = 'solemp-core/target/release/solemp_core.dll'
            new_path = 'solemp-godot/bin/release/solemp_core.dll'
            _move_file(old_path, new_path)

        case CompilationFlags.DEBUG:
            old_path = 'solemp-core/target/debug/solemp_core.dll'
            new_path = 'solemp-godot/bin/debug/solemp_core.dll'
            _move_file(old_path, new_path)

        case CompilationFlags.RELEASE_BUILD:
            _build_cargo("release")

        case CompilationFlags.DEBUG_BUILD:
            _build_cargo("debug")

        case _:
            print("Unimplemented flag")
            return

def _build_cargo(flag: str):
    # Start building with command in solemp-core directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    cargo_dir = os.path.join(project_root, "solemp-core")

    # Start build or release command depend on flag 
    command = ["cargo", "build"]
    if flag == "release":
        command.append("--release")

    print(f"Running {' '.join(command)} in {cargo_dir}...")

    try:
        subprocess.run(command, cwd=cargo_dir, check=True)
        print("Cargo build finished successfully!") 
    except subprocess.CalledProcessError:
        print("Error: Cargo build failed!")
    except FileNotFoundError:
        print("Error: 'cargo' command not found. Cheak Rust intstallation")

def _move_file(old_path, new_path):
    # Moving files from old path to new path
    try:
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        os.rename(old_path, new_path)
        print(f"File successful moved. From -> {old_path} to {new_path}")
    except FileNotFoundError:
        print(f"File -> {old_path} not found")
    except PermissionError:
        print("No access rights")