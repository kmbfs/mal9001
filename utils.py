import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_delay(command, secs):
    return f"sleep {secs}; "+command
