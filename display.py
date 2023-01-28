import re
import os
from art import tprint
from time import sleep
from utils import *
from audio import read_aloud

def blue_input(text):
    return input(colorize(39, text))

def bold(text, say=True, say_wait=False, voice=None):
    print('\033[1m' + text + '\033[0m')

    if say:
        read_aloud(text, wait=say_wait, no_numbers=True, voice=voice)

def italics(text):
    print('\x1B[4m' + text + '\x1B[4m')

def colorize(color_, x):
    if color_ is None:
        return x
    return f"\033[38;5;{str(color_)}m{str(x)}\033[0;0m"

def decolorize(x):
    x = x.replace("\033[38;5;", "").replace("\033[0;0m", "")
    x = re.sub(r'\d+m', '', x, count=1)
    return x

def colors_16(color_):
    return("\033[2;{num}m {num} \033[0;0m".format(num=str(color_)))

def colors_256(color_):
    return colorize(color_, color_)

def matrix_fill(color_=47):
    for _ in range(os.get_terminal_size().lines):
        matrix_line(color_=color_)

def matrix_line(color_=47):
    chars = [pick_random(P_MATRIX_SHUFFLE) for _ in range(os.get_terminal_size().columns)]
    print(colorize(color_, "".join(chars)), end="\r")

def matrix_shuffle(text, wait, color_=47):
    full = ""
    for i,c in enumerate(text):
        l = [pick_random(P_MATRIX_SHUFFLE) for _ in range(len(text)-1)]
        for j in range(i):
            l[j] = text[j]
        print(colorize(color_, "".join(l)), end="\r")
        sleep(wait)
    print("".join(l))

def show_process(wait, iterations, proc_type, color=None):
    for i in range(iterations):
       sleep(wait)
       if color:
           # color = 50
           print(colorize(color,f"{proc_type[i%len(proc_type)]}"), end="\r")
       else:
           print(f"{proc_type[i%len(proc_type)]}", end="\r")

def rightwards_completion(color_=None, wait=WAIT_ULTRAFAST):
    cols = os.get_terminal_size().columns
    for i in range(cols):
        l = [" " if _ > i else "=" for _ in range(cols)]
        l[i] = ">"
        print(colorize(color_, "".join(l)), end="\r")
        sleep(wait)
    print(colorize(color_, "".join(l)))

def bounce(color_=None, wait=WAIT_ULTRAFAST, iterations=3):
    cols = os.get_terminal_size().columns
    for x in range(iterations):
        for i in range(cols*2):
            l = [" " for _ in range(cols)]
            if i >= cols:
                i = cols - i%cols - 1
            l[i] = "*"
            print(colorize(color_, "".join(l)), end="\r")
            sleep(wait)
    print("", end="\r")

def percentage(color_=None):
    l = [" "," "," "," "]
    for i in range(100+1):
        for x,j in enumerate(str(i)):
            l[x] = j
        l[x+1] = "%"

        if i < 50:
            print(colorize(color_, "".join(l)), end="\r")
            sleep(WAIT_ULTRAFAST)

        elif i < 80:
            print(colorize(color_, "".join(l)), end="\r")
            sleep(WAIT_FAST)

        elif i < 90:
            print(colorize(color_, "".join(l)), end="\r")
            sleep(WAIT_ULTRAFAST)

        else:
            print(colorize(color_, "".join(l)), end="\r")
            sleep(WAIT_SENTENCE)

def whisper(text):
    print(colorize(234, text))

def slow_print(text, wait, color_=None, charwise=False):
    full = ""

    if " " in text and not charwise:
        for s in text.split(" "):
            full = full + s + " "
            print(colorize(color_, full), end="\r")
            sleep(wait)
    else:
        for s in text:
            full = full + s
            print(colorize(color_, full), end="\r")
            sleep(wait)
    print("\n")


### demo functionality

def initialize():
    print("The 16 colors scheme is:")
    print(' '.join([colors_16(x) for x in range(30, 38)]))
    print("\nThe 256 colors scheme is:")
    print(' '.join([colors_256(x) for x in range(256)]))

def demo():
    print("terminal width", os.get_terminal_size().columns)
    initialize()
    whisper("Shh. Beginning demo")
    slow_print("The demo is starting shortly", WAIT_SENTENCE)
    slow_print("The demo is starting shortly", WAIT_WORD, charwise=True)
    slow_print("Waiting", WAIT_WORD)
    matrix_shuffle("Welcome to the MAL program.", WAIT_FAST)
    x = input(colorize(92, "What's your name?"))
    print("Hi", colorize(39, x))
    show_process(WAIT_PROGRESS,WAIT_PROGRESS_ITERS,P_WHEEL)
    y = input("What's your name?")
    print("Hi", y)
    show_process(WAIT_PROGRESS,WAIT_PROGRESS_ITERS,P_THINK)

def test_effects():
    rightwards_completion()
    bounce()
    percentage()
    stops_at_99_percent_for_a_comedicly_long_time()

def logo():
    tprint("MAL 9001","alpha")
    tprint("MAL 9001","block2")
    tprint("MAL 9001","cyberlarge")
    tprint("MAL","dotmatrix")
    tprint("MAL 9001","graceful")
    tprint("MAL 9001","isometric2")
    tprint("MAL","lean")
    tprint("MAL 9001","lineblocks")
    tprint("MAL POOI","sub-zero")
    tprint("MAL 9001","nipples")
    tprint("MAL 9001","rounded")
    tprint("MAL 9001","varsity")

def print_logo():
    cols = os.get_terminal_size().columns
    print("~"*cols)
    print("~"*cols)
    print("\n")
    tprint("MAL 9001","rounded")
    bold("'MAL 9001 Marriage Automation Liaison Software Interface'")
    print("© 2001 Cinco Corporation, LLC. All rights reserved.\n\n")
    print("~"*cols)
    print("~"*cols)
