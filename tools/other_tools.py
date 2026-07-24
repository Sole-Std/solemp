import os

def _console_clear_():
    os.system('cls' if os.name == 'nt' else 'clear')