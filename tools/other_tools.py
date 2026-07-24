import os
import platform
import sys

def _console_clear_():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_os_type() -> str:
    os_name = platform.system().lower()
    
    if os_name == "windows":
        return "windows"
    
    if os_name == "linux":
        return "linux"
    
    if os_name == "darwin":
        machine = platform.machine().lower()
        if "arm" in machine or "aarch64" in machine:
            return "macos_arm"
        return "macos"
    
    return "unknown"