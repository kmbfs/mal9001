import os
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_delay(command, secs):
    return f"sleep {secs}; "+command

def make_warning_sound():
    pro = subprocess.Popen(['tput bel'],
                           shell=True)
