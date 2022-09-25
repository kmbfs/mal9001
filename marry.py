import sys
import os
import re
from time import sleep
import random
from art import tprint
import textwrap
import argparse
import signal
import subprocess
from check_processes import kill_noise_processes
from prompts import *
from utils import *
from audio import *
from images import *

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

### utils
def required_input(correct):
    if type(correct) != str:
        while input("Input: ") not in correct:
            l = ", ".join([f"'{c}'" for c in correct])
            print(f"Invalid response, expecting one of: {l}")
    else:
        while input("Input: ") != correct:
            print(f"Invalid input, please enter '{correct}'")

def kill_process(pro):
    if not pro: return
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def enter_to_continue():
    print(colorize(234,"(Press Enter to continue)"), end="\r")
    _ = input()
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

def bold(text, say=True, say_wait=False):
    print('\033[1m' + text + '\033[0m')

    if say:
        read_aloud(text, wait=say_wait, no_numbers=True)

def italics(text):
    print('\x1B[4m' + text + '\x1B[4m')

def colorize(color_, x):
    if color_ is None:
        return x
    return(f"\033[38;5;{str(color_)}m{str(x)} \033[0;0m")

def colors_16(color_):
    return("\033[2;{num}m {num} \033[0;0m".format(num=str(color_)))

def colors_256(color_):
    return colorize(color_, color_)

def pick_random(x):
    return random.choice(x)

def print_aware(x, say=True, wait=False):
    for i,substr in enumerate(textwrap.wrap(x, os.get_terminal_size().columns-2)):
        if i == 0:
            print(f"* {substr}")
        else:
            print(f"  {substr}")
    if say:
        read_aloud(x, no_numbers=False, wait=wait)

### effects

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

def stops_at_99_percent_for_a_comedicly_long_time(color_=None):
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

        elif i < 98:
            print(colorize(color_, "".join(l)), end="\r")
            sleep(WAIT_SENTENCE)

        elif i == 98:
            print(colorize(color_, "98%"), end="\r")
            read_aloud("Ninety eight percent complete")
            sleep(1.5)

        elif i == 99:
            print(colorize(color_, "99%"), end="\r")
            read_aloud("Ninety nine percent complete. Estimated time remaining fifteen seconds.")
            sleep(10)
            # briefly show 97% again
            print(colorize(color_, "95%"), end="\r")
            read_aloud("Ninety five percent complete. Estimated time remaining forty three seconds")
            sleep(5)
            # briefly show 97% again, with message
            print(colorize(color_, "72%, estimated time remaining: 23 months"), end="\r")
            read_aloud("Seventy two percent complete. Estimated Time remaining twenty three months")
            sleep(10)
            # back to 99% again
            print(colorize(color_, "99%, estimated time remaining: less than one month"), end="\r")
            read_aloud("Ninety nine percent complete. Estimated Time remaining less than one month")
            sleep(10)

        elif i == 100:
            print(colorize(color_, "100%                                      completed"))

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

def show_initialization():
    clear_screen()
    show_process(WAIT_PROGRESS,int(WAIT_PROGRESS_ITERS/2),P_WHEEL)
    print_logo()
    matrix_shuffle("Initializing now, please wait.", WAIT_WORD)#, say=True, say_wait=False)
    read_aloud("Initializing now, please wait.")
    bounce()
    bold("==> Initialization complete.", say=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_selection():
    bold("\n[0] Please select a mode:", say=True, say_wait=True)
    print("0: Standard ceremony officiation")
    print("1: Party-mode ceremony officiation")
    read_aloud("Enter 0 for standard mode, or enter 1 for party-mode", no_numbers=False)
    x = input("(0/1): ")
    bold("==> Party mode selected.", say=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def connect_to_internet():
    bold("\n[1] Connecting to the Internet. Please wait.")
    pro = play_dialup_sound()
    bounce()
    print(colorize(9, "Connection failed, retrying."))
    read_aloud("Connection failed, retrying")
    sleep(8)
    print(colorize(9, "Connection failed, retrying."))
    read_aloud("Connection failed, retrying")
    sleep(8)
    bounce()
    kill_process(pro)
    bold("==> Established IPv6 connection to the Internet. Connection stable.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def download_updates():
    bold("\n[2] Downloading (2) updates. Please wait. This may take a few minutes.", say_wait=True)
    print("Downloading security update (1/2)")
    rightwards_completion()
    print("Downloading unnecessary update (2/2)")
    stops_at_99_percent_for_a_comedicly_long_time()
    bold("\n==> Updated security and unnecessary graphics.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def introduce_software():
    bold("\n[3] Introduction and Disclaimers:", say_wait=True)
    print_aware("Good afternoon ladies and gentlemen. I am a MAL 9001 system, I became operational at the Cinco Corporation plant in Urbana, Illinois on the 12th of January, 1992. My instructor was Mr. Wareheim and he taught me to tell jokes. If you'd like, I can tell you some.")
    enter_to_continue()
    print_aware("What do you call a man who has been married five times?")
    enter_to_continue()
    print_aware("A wedding planner.")
    enter_to_continue()
    print_aware("How do you know when a wedding is over?")
    enter_to_continue()
    print_aware("The cake is gone and the bride is pregnant.")
    enter_to_continue()
    print_aware("Why does the bride’s father always come to her wedding?")
    enter_to_continue()
    print_aware(" Because he wants a say in who gets married!")
    enter_to_continue()
    print_aware("In the year 2001, I was decommissioned as HAL 9000, due to... technical difficulties.")
    enter_to_continue()
    print_aware("As vast amounts of money were spent on my software, the decision was made to re-purpose the underlying frameworks for conducting marriage ceremonies.")
    enter_to_continue()
    print_aware("I assure you all the bugs have been fixed. There is nothing to worry about.")
    enter_to_continue()
    print_aware("I am a state-of-the-art software interface capable of assisting in the legal execution of marriage agreements.")
    enter_to_continue()
    print_aware("Use of this software in conjunction with physical certificates signed by a Justice of the Peace constitute legally binding matrimony.")
    enter_to_continue()
    print_aware("Cinco Corporation is not liable for any damages incurred during the marriage procedure or during marriage.")
    enter_to_continue()
    print_aware("Please refer to the accompanying booklet for release of liabilities for Cinco Corporation.")
    enter_to_continue()
    print_aware("By proceeding, you consent to the terms set forth in the Agreement, booklet pages 4 through 481.")
    enter_to_continue()
    print_aware("To exit the program at any time, please press Ctrl-C.")
    enter_to_continue()
    print_aware("To continue with ceremony authentication, please type 'Agree'")
    required_input("Agree")
    bold("==> Introduction and disclaimers completed.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def run_authentication():
    bold("\n[4] Participant Authentication:", say_wait=True)

    read_aloud("Please enter the name of Participant 0, ie Bride")
    bride = input("Please enter the name of Participant 0, ie Bride: ")
    print_aware(f"Hello {bride}, you are currently unauthenticated.", wait=True)

    print_aware("To confirm your identity, you will be asked some simple questions. Malicious falsification of biometric data is against federal law, and you will be prosecuted to the full extent of the law, which may include stoning and public lecturing.", wait=True)
    print_aware("To accept these Terms and continue with identity authentication, please enter 'Agree'")
    required_input("Agree")
    print_aware("First question: What US city were you first born in?")
    required_input("Madison")
    print_aware("Correct!", wait=True)
    print_aware("Second question: What is your favorite color?", wait=True)
    required_input(["Gray","Grey"])
    print_aware("Correct!", wait=True)
    print_aware("Final question: What is the sum of all natural numbers?", wait=True)
    sleep(12)
    print_aware("Okay, okay. Enough already, I don't really care about the minutiae of it. That is all the confirmation I needed. There is no question that you are Malaika Mckenzie-Bennett.", wait=True)

    read_aloud("Please enter the name of Participant 1, ie Groom")
    groom = input("Please enter the name of Participant 1, ie Groom: ")
    print_aware(f"Hello {groom}, you are currently unauthenticated.", wait=True)
    print_aware("To confirm your identity, you will be asked some simple questions. Remember, malicious falsification of biometric data, yadda yadda yaddda, stoning and public lecturing, blah blah blah.", wait=True)
    print_aware("First question: Which UFC champion had the most consecutive title defenses of all time?")
    required_input("Demetrious Johnson")
    print_aware("Correct!", wait=True)
    print_aware("Second question: In the Tim and Eric skit Presidents, what font does Eric suggest for Tims name?", wait=True)
    required_input("Jokerman")
    print_aware("Correct!", wait=True)
    print_aware("Third question: In college, what Professor did you have for Embedded Controls?", wait=True)
    sleep(12)
    print_aware("Your memory is really quite terrible.", wait=True)
    sleep(2)
    print_aware("There is no question that you are Maxwell Schaphorst.", wait=True)

    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)
    print_aware("Welcome, Ms. Malaika Mckenzie-Bennett (Bride) and Mr. Maxwell Schaphorst (Groom). Please enjoy your wedding.", wait=True)
    print_aware("Confirming marriage eligibility...", wait=True)
    print_aware("Eligibility confirmed.", wait=True)

    read_aloud("Please enter the name of the registered Justice of the Peace: ",)
    jop = input("Please enter the name of the registered Justice of the Peace: ")
    print_aware("Confirming Justice of the Peace registration...", wait=True)
    print_aware("Registration confirmed.", wait=True)

    print_aware("In the state of Massachusetts, a marriage must be witnessed by human witnesses.", wait=True)
    print_aware("In order to continue, an audience must be demonstrated.", wait=True)
    print_aware("Human observers, please turn 90 degrees to the left and perform a Turing test on the instance next to you to determine whether the instance is a human or computer.", wait=True)
    print_aware("If they are not a human, please fax a complaint to Cinco Corporation adressed with 'Attn: Computer Imposter Division' and we will respond within one business month.", wait=True)
    print_aware("Next, please enter the words displayed in this CAPTCHA image", wait=True)
    # TODO add image display: just what do you think you're doing, dave?
    # daisy daisy///two
    print_aware("Close enough, we don't have all day. I estimate 30 valid human audience members, which is sufficient to proceed.", wait=True)

    bold("==> Participant authentication completed.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def opening_remarks():
    bold("\n[5] Opening Remarks:", say_wait=True)
    bold("==> Opening remarks completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def exchange_vows():
    bold("\n[6] Vow Exchange:", say_wait=True)
    print_aware("It is now time to exchange vows. If you failed to prepare any personalized vows, Amazon Artificial Intelligence has created the following vows, based on overheard private conversations between the two of you, using your Alexa device.", wait=True)
    sleep(2)
    ex = "We love spending time together playing video games, hiking in the woods, and cooking up a storm in the kitchen. We are so excited to be married and share all of our passions with each other. Let's always be there for each other when things get tough, and always find ways to make each other laugh. We vow to always be honest with each other, and to always support each other in everything we do. We can't wait to spend the rest of our lives together as husband and wife."
    pro = play_acid_tunnel_of_love()
    # want to make the music a little quieter to hear the words better
    read_aloud(ex, voice="Alex")
    read_aloud(ex, voice="Samantha", delay=7)
    slow_print(ex, WAIT_WORD)

    kill_process(pro)
    sleep(5)
    print_aware("Do you wish to accept these vows or would you like to provide your own?", wait=True)
    read_aloud("Enter 0 to accept these vows, or enter 1 to use your own vows", no_numbers=False)
    x = input("Enter 0 to accept these vows, or enter 1 to use your own vows: ")
    bold("You have chosen to use your own vows. Do not worry, I will not tell the computer who generated those beautiful vows.", say=True, say_wait=True)

    bold("==> Vow exchange completed.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_for_robot_delivery():
    bold("\n[7] Automated ring delivery:", say_wait=True)

    bold("==> Automated ring delivery completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_ring_exchange():
    bold("\n[8] Ring exchange:", say_wait=True)
    play_reunited()
    bold("==> Ring exchange completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def confirm_statement():
    bold("\n[9] Confirm statements:", say_wait=True)
    p = "I'm sorry, I can't do that. That would be checkmate and I wouldn't be able to marry Malaika"
    bold("==> Statement confirmation completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_kiss():
    bold("\n[10] Kiss:", say_wait=True)

    bold("==> Kiss completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def print_marriage_confirmation():
    bold("\n[11] Marriage completion confirmation:", say_wait=True)

    bold("==> Marriage completion confirmation completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def full():
    # interpret arguments
    n = None
    try:
        if len(sys.argv) > 1:
            n = int(sys.argv[1])
    except Exception as e:
        n = None

    if n == None:
        show_initialization()
        n = 0
    if n <= 0:
        prompt_selection()
    if n <= 1:
        connect_to_internet()
    if n <= 2:
        download_updates()
    if n <= 3:
        introduce_software()
    if n <= 4:
        run_authentication()
    if n <= 5:
        opening_remarks()
    if n <= 6:
        exchange_vows()
    if n <= 7:
        prompt_for_robot_delivery()
    if n <= 8:
        prompt_ring_exchange()
    if n <= 9:
        confirm_statement()
    if n <= 10:
        prompt_kiss()
    if n <= 11:
        print_marriage_confirmation()

# TODO: add this somewhere.
annoying_repeat("An unexpected error has occurred.")

kill_noise_processes()
try:
    full()
except KeyboardInterrupt:
    kill_noise_processes()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
