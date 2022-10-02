import os
import random

P_WHEEL = "|/-\\"
P_THINK = ["   ",".  ",".. ","..."]
P_ODD = "0100111001?"
P_MATRIX_SHUFFLE = "ABCDEFGHIJKLMNOPQRSTUVQXYZ12345678910!@#$%^&*()-_+="
WAIT_WORD = 0.3
WAIT_SENTENCE = 0.4
WAIT_PROGRESS = 0.2
WAIT_PROGRESS_ITERS = 50
WAIT_FAST = 0.1
WAIT_ULTRAFAST = 0.01
WAIT_FASTEST = 0.001
WAIT_PROGRESS_INTER_SECTION = 5

errors = [
    "no such file or directory",
    "list index out of range",
    "KeyError",
]

def pick_random(x):
    return random.choice(x)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
