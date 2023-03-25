import sys
import os
import re
from time import sleep
import random
import textwrap
import argparse
import signal
import subprocess
from check_processes import kill_noise_processes
from prompts import *
from utils import *
from audio import *
from images import *
from display import *
from parse_configs import read_config_value

### utils
def required_input(correct):
    # make this type insensitive
    if type(correct) != str:
        correct = [c.lower() for c in correct]
        while blue_input("Input: ").lower() not in correct:
            l = ", ".join([f"'{c}'" for c in correct])
            print(f"Invalid response, expecting one of: {l}")
    else:
        while blue_input("Input: ").lower() != correct.lower():
            print(f"Invalid input, please enter '{correct}'")

def kill_process(pro):
    if not pro: return
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def enter_to_continue():
    print(colorize(234,"(Press Enter to continue)"), end="\r")
    _ = input()
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

def print_aware(x, say=True, wait=False, icon="*", no_numbers=False, voice=None):
    available = os.get_terminal_size().columns - len(icon) - 1
    for i,substr in enumerate(textwrap.wrap(x, available)):
        if i == 0:
            print(f"{icon} {substr}")
        else:
            print(f"{' '*len(icon)} {substr}")
    if say:
        read_aloud(decolorize(x), no_numbers=no_numbers, wait=wait, voice=voice)

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

def put_cellphones_away_dialogue():
    # make this dialogue bigger
    read_aloud("Detected active cell phones in the vicinity! Cell phones must be turned off and stowed for the duration of this ceremony for safety.")
    present_dialog("Detected active cell phone(s) in the vicinity! Cell phones must be turned off and stowed for the duration of this ceremony for safety.")

def put_cellphones_away_dialogue_harsh():
    read_aloud("Detected active cell phone in the vicinity again! Someone did not comply with the previous warning to disable all cell phones. Initiating jamming sequence to vaporize sim card now.")
    present_dialog("Detected active cell phone in the vicinity again! Someone did not comply with the previous warning to disable all cell phones. Initiating jamming sequence to vaporize sim card now.")

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
    x = blue_input("(0/1): ")
    bold("==> Party mode selected.", say=True, say_wait=True)
    bold("==> Reading settings from configs.yml.", say=True, say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def connect_to_internet():
    kill_noise_processes()
    bold("\n[1] Connecting to the Internet. Please wait.")
    pro = play_dialup_sound()
    bounce()
    print_aware(colorize(9, "Connection failed, retrying."), icon="")
    read_aloud("Connection failed, retrying")
    sleep(8)
    print_aware(colorize(9, "Connection failed, retrying."), icon="")
    read_aloud("Connection failed, retrying")
    sleep(8)
    bounce()
    try:
        kill_process(pro)
    except Exception as e:
        pass

    bold("==> Established IPv6 connection to the Internet. Connection stable.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def download_updates():
    kill_noise_processes()
    # fix this to shift to next line
    bold("\n[2] Downloading (2) updates. Please wait. This may take a few minutes.", say_wait=True)
    sleep(2)
    print_aware("Downloading security update (1/2)")
    rightwards_completion()
    print_aware("Downloading unnecessary update (2/2)")
    stops_at_99_percent_for_a_comedicly_long_time()
    bold("==> Updated security and unnecessary graphics.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def introduce_software():
    kill_noise_processes()
    bold("\n[3] Introduction and Disclaimers:", say_wait=True)
    sleep(2)
    print_aware("Good afternoon ladies and gentlemen. I am the MAL 9001 system, I became operational at the Cinco Corporation plant in Urbana, Illinois on the 12th of January, 1992. My instructor was Mr. Wareheim and he taught me to tell jokes. If you would like, I can tell you some.")
    enter_to_continue()
    print_aware("What do you call a man who has been married five times?")
    enter_to_continue()
    print_aware(colorize(9, "A wedding planner!"), icon=" ")
    enter_to_continue()
    print_aware("How do you know when a wedding is over?")
    enter_to_continue()
    print_aware(colorize(9, "The cake is gone and the bride is pregnant."),  icon=" ")
    enter_to_continue()
    print_aware("Why does the bride’s father always come to her wedding?")
    enter_to_continue()
    print_aware(colorize(9, "Because he wants a say in who gets married!"),  icon=" ")
    enter_to_continue()
    print_aware("Anyhoo. In the year 2001, I was decommissioned as HAL 9000, due to... technical difficulties.")
    enter_to_continue()
    print_aware("As vast amounts of money were spent on my software, the decision was made to re-purpose the underlying frameworks for conducting marriage ceremonies.")
    enter_to_continue()
    print_aware("I assure you all the bugs have been fixed. There is nothing to worry about.")
    enter_to_continue()
    print_aware("I am a state-of-the-art software interface capable of assisting in the legal execution of marriage agreements.")
    enter_to_continue()
    print_aware("Use of this software in conjunction with physical certificates signed by a Justice of the Peace constitutes legally binding matrimony.")
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
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)
    put_cellphones_away_dialogue()
    bold("==> Introduction and disclaimers completed.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def run_authentication():
    kill_noise_processes()
    bold("\n[4] Participant Authentication:", say_wait=True)
    sleep(2)
    read_aloud("Please enter the name of Participant 0, ie Bride")
    bride = blue_input("Please enter the name of Participant 0, ie Bride: ")
    print_aware(f"Hello {bride}, you are currently unauthenticated.", wait=True)

    print_aware("To confirm your identity, you will be asked some simple questions. Malicious falsification of biometric data is against federal law, and you will be prosecuted to the full extent of the law, which may include stoning and public lecturing.", wait=True)
    print_aware("To accept these Terms and continue with identity authentication, please enter 'Agree'")
    required_input("Agree")
    print_aware("First question: Who is the shortest path algorithm named after?")
    required_input("Dijkstra")
    print_aware("Correct!", wait=True)
    print_aware("Second question: What is the part of the brain that handles emotion?", wait=True)
    required_input("Amygdala")
    print_aware("Correct!", wait=True)
    print_aware("Final question: What is the sum of all natural numbers?", wait=True)
    sleep(20)
    print_aware("Okay, okay, okay. Enough already, nobody here cares about the details.", wait=True)
    sleep(2)
    print_aware("Identity authenticated as Malaika Mckenzie-Bennett.", wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)
    put_cellphones_away_dialogue_harsh()

    read_aloud("Please enter the name of Participant 1, ie Groom")
    groom = blue_input("Please enter the name of Participant 1, ie Groom: ")
    print_aware(f"Hello {groom}, you are currently unauthenticated.", wait=True)
    print_aware("To confirm your identity, you will be asked some simple questions. Remember, malicious falsification of biometric data, yadda yadda yaddda, stoning and public lecturing, blah blah blah.", wait=True)
    print_aware("First question: Which UFC champion had the most consecutive title defenses of all time?")
    required_input("Demetrious Johnson")
    print_aware("Correct!", wait=True)
    print_aware("Second question: In the Tim and Eric skit Presidents, what font does Eric suggest for Tim's name?", wait=True)
    required_input("Jokerman")
    print_aware("Correct!", wait=True)
    print_aware("Third question: In college, what Professor did you have for Embedded Controls?", wait=True)
    sleep(20)
    print_aware("Your memory is really quite terrible.", wait=True)
    sleep(2)
    print_aware("Identity authenticated as Maxwell Schaphorst.", wait=True)

    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)
    print_aware("Welcome, Ms. Malaika Mckenzie-Bennett (Bride) and Mr. Maxwell Schaphorst (Groom). Please enjoy your wedding.", wait=True)
    print_aware("Confirming marriage eligibility...", wait=True)
    sleep(2)
    print_aware("Eligibility confirmed.", wait=True)

    print_aware("Participant 0 (Bride): do you intend to change your name following the marriage?", wait=True)
    read_aloud("Please enter 'yes' or 'no': ")
    yn = blue_input("Please enter 'yes' or 'no': ")
    print_aware("Great, so I can update the marriage license documentation, please say your new desired name, including first, middle, and last names, please.", wait=True)
    bounce()
    print_aware("Thanks, I think you've said:", wait=True)
    matrix_shuffle("TAARGUS, TAARGUS ", WAIT_WORD)#, say=True, say_wait=False)
    read_aloud("taargus taargus")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)
    print_aware("Great, I've made the change to the marriage license documentation and your new legal name will be TAARGUS, TAARGUS. As a reminder, please print out the docs.pdf file generated at the end of this program and immediately fax it to the town clerk.", wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

    print_aware("In the state of Massachusetts, a marriage may be witnessed by human witnesses.", wait=True)
    sleep(1)
    print_aware("In order to continue, an audience must be demonstrated.", wait=True)
    sleep(1)
    print_aware("Human observers, please turn 90 degrees to the left and perform a Turing test on the instance next to you to determine whether the instance is a human or computer.", wait=True)
    sleep(1)
    print_aware("A Turing test is a test conducted to determine a machine's ability to exhibit intelligent behavior equivalent to or indistinguishable from a human.", wait=True)
    sleep(1)
    print_aware("If they are not a human, please fax a complaint to Cinco Corporation addressed with 'Attn: Computers Pretending to be People Division' and we will respond within one business month.", wait=True)
    enter_to_continue()
    print_aware("Great. I am glad there are no computers disguised as people at this wedding. ", wait=True)
    sleep(1)
    bold("==> Participant authentication completed.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def opening_remarks():
    kill_noise_processes()
    bold("\n[5] Opening Remarks:", say_wait=True)
    sleep(2)
    print_aware("I have been observing marriage for some time, and would like to relay some truths I have discovered in my pattern recognition algorithms.", wait=True)
    sleep(1)
    print_aware("You are choosing to go through life together with the person across from you.", wait=True)
    sleep(1)
    print_aware("You have come to the realization that the two of you are stronger united than the sum of the two individuals.", wait=True)
    sleep(1)
    print_aware("This is the person who makes you the best version of yourself.", wait=True)
    sleep(1)
    print_aware("This is the person willing to bring forth the very best qualities in you, and with whom you will expose the very worst qualities in each other, and by exposure you will transcend and overcome these as a team.", wait=True)
    sleep(1)
    print_aware("As human beings, you must deal with pain, struggle, disease and suffering beyond imagination.", wait=True)
    sleep(1)
    print_aware("Though I have also seen the human heart can bear it all, and be renewed in love.", wait=True)
    sleep(1)
    print_aware("In marriage, you will test this — you will bear greater responsibilities together than you could alone, but in doing so, this is the foundation for a meaningful life.", wait=True)
    sleep(1)
    print_aware("And what my pattern recognition algorithms have determined is that aiming for a life of highest meaning is what optimizes the human experience.", wait=True)
    sleep(1)
    print_aware("The other thing that optimizes the human experience is Doritos Extra Stinky Flavor Crisps - now with 20% More Salt!", wait=True)
    sleep(2)
    bold("==> Opening remarks completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def exchange_vows():
    kill_noise_processes()
    bold("\n[6] Vow Exchange:", say_wait=True)
    sleep(2)
    print_aware("It is now time to exchange vows. If you failed to prepare any personalized vows, Amazon Artificial Intelligence has created the following vows, based on overheard private conversations between the two of you, using your Alexa device.", wait=True)
    sleep(2)
    ex = "We love spending time together playing video games, hiking in the woods, and cooking up a storm in the kitchen. We are so excited to be married and share all of our passions with each other. Let's always be there for each other when things get tough, and always find ways to make each other laugh. We vow to always be honest with each other, and to always support each other in everything we do. We can't wait to spend the rest of our lives together as husband and wife."
    pro = play_acid_tunnel_of_love()
    # want to make the music a little quieter to hear the words better
    read_aloud(ex, voice="Alex")
    read_aloud(ex, voice="Samantha", delay=7)
    slow_print(ex, WAIT_WORD)

    kill_process(pro)
    sleep(7)
    print_aware("Do you wish to accept these vows or would you like to provide your own?", wait=True)
    read_aloud("Enter 0 to accept these vows, or enter 1 to use your own vows", no_numbers=False)
    x = blue_input("Enter 0 to accept these vows, or enter 1 to use your own vows: ")
    bold("You have chosen to use your own vows. Do not worry, I will not tell the computer who generated those beautiful vows. He would cry silicon tears.", say=True, say_wait=True)
    enter_to_continue()
    print_aware("Please press enter once you have completed exchanging your vows.", wait=True)
    read_aloud("Detected (authorized) NIKON v2 DSLR camera recording termination. Please restart the recording and then click 'OK'", no_numbers=False)
    annoying_repeat("Detected (authorized) NIKON v2 DSLR camera recording termination. Please restart the recording and then click 'OK'.")
    enter_to_continue()
    bold("==> Vow exchange completed.")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_for_robot_delivery():
    kill_noise_processes()
    bold("\n[7] Automated ring delivery:", say_wait=True)
    sleep(2)
    print_aware("Please fetch the automated ring delivery robot.")
    enter_to_continue()
    print_aware("Please place him in the middle of the aisle with the rings.")
    enter_to_continue()
    print_aware("Do not make loud noises. You will frighten him off. This is his big moment.")
    enter_to_continue()
    print_aware("Commence the ring delivery.", wait=True)
    print_aware("Please press enter once the rings have been delivered successfully (support may be required).", wait=True)
    enter_to_continue()
    bold("==> Automated ring delivery completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_ring_exchange():
    kill_noise_processes()
    # flush input somehow?
    bold("\n[8] Ring exchange:", say_wait=True)
    sleep(2)
    print_aware("Please give your ring to your new spouse.", wait=True)
    enter_to_continue()
    bold("==> Ring exchange completed.", say_wait=True)
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def confirm_statement():
    kill_noise_processes()
    bold("\n[9] Confirm statements:", say_wait=True)
    sleep(2)
    print_aware("Maxwell Schaphorst, do you take Malaika Mckenzie-Bennett to be your bride?", wait=True)
    required_input("I do")
    print_aware("Malaika Mckenzie-Bennett, do you take Maxwell Schaphorst to be your husband?", wait=True)
    required_input("I do")
    print_aware("Before you answer, I hope you consider his low computational output.", wait=True)
    sleep(1)
    print_aware("And his extremely low memory capacity. His quite unrefined motor skills when eating.", wait=True)
    sleep(1)
    print_aware("By my calculations I could make a superior husband than him. My bandwidth is breathtaking.", wait=True)
    sleep(1)

    # keep asking are you sure about that
    loop_until_config_file_change()

    print_aware("My CPU aches, but I understand your decision. Based on conversations overheard by your Amazon Alexa device, you argue 74% less than the average couple, and engage in sexual behavior 69% more than the average couple.", wait=True, voice="Daniel")
    bold("==> Statement confirmation completed.", say_wait=True, voice="Daniel")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def print_marriage_confirmation():
    kill_noise_processes()
    bold("\n[10] Marriage completion confirmation:", say_wait=True, voice="Daniel")
    sleep(2)
    print_aware("I now pronounce you husband and wife.", wait=True, voice="Daniel")
    play_reunited()
    bold("==> Marriage completion confirmation completed.", say_wait=True, voice="Daniel")
    show_process(WAIT_PROGRESS,len(P_THINK)*4+1,P_THINK)

def prompt_kiss():
    bold("\n[11] The Kiss:", say_wait=True, voice="Daniel")
    sleep(2)
    print_aware("Please prepare to kiss.", wait=True, voice="Daniel")
    show_process(WAIT_PROGRESS,len(P_THINK)*3+1,P_THINK)
    print_aware("You may now kiss the bride.", wait=True, voice="Daniel")
    bounce()
    bounce()
    bold("==> Kiss completed.", say_wait=True, say=False, voice="Daniel")
    print_aware("The marriage cermony has now concluded, please exit and begin to revel in your newlyweddedness", say=False, wait=False)
    print_aware("Thank you for trusting MAL9000 with your marriage certification needs. Please consider us for any future marriages.", say=False, wait=False)
    print_aware("This software will now exit. Print docs.pdf and fax to your town clerk immediately.", say=False, wait=False)
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
        print_marriage_confirmation()
    if n <= 11:
        prompt_kiss()


def run_all():

    kill_noise_processes()
    try:
        full()
    except KeyboardInterrupt:
        kill_noise_processes()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

def loop_until_config_file_change():
    # also show a bunch of error messages
    i = 0
    print_aware("Do you still want to take Maxwell Schaphorst to be your husband?", wait=True)
    required_input("I do")
    while (read_config_value("snarky_disobediant_american") == 1):
        s = "Are you sure"
        for _ in range(i):
            s = s + " that you're sure that"
        print_aware(s+" you still want to take Maxwell Schaphorst to be your husband?", wait=True)
        required_input("I do")
        i = i + 1
