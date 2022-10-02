import os
import re
import subprocess
from time import sleep
from utils import add_delay, make_warning_sound

def format_osascript_buttons(buttons):
    buttons_s = ",".join([f'\"{s}\"' for s in buttons])
    button_types = "default button 1"
    if len(buttons) > 1:
        button_types = button_types + " cancel button 2"
    return "buttons {"+ buttons_s +"} "+ button_types

def present_dialog(
    text,
    buttons=["OK"],
    wait=True,
    wait_seconds=900,
    icon="stop",
    delay=0,
):
    t = "osascript -e 'tell application (path to frontmost application as text) to display dialog \""
    t = t + text +"\" "
    t = t + format_osascript_buttons(buttons)
    t = t + " with icon " + icon
    t = t + " giving up after " + str(wait_seconds)
    t = t + "'"
    t = add_delay(t, delay)
    pro = subprocess.Popen([t], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    if wait:
        pro.wait()

def present_alert(
    text,
    sub_message="Program is unstable and may terminate at any time.",
    buttons=["OK"],
    wait=True,
    wait_seconds=900,
):
    t = "osascript -e 'tell application (path to frontmost application as text) to display alert \""
    t = t + text +"\" message \""+sub_message+"\" as critical "
    t = t + format_osascript_buttons(buttons) + " giving up after "+str(wait_seconds)
    t = t + "'"
    make_warning_sound()
    pro = subprocess.Popen([t], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    if wait:
        pro.wait()

def annoying_repeat(text, sub_message="Program is unstable and may terminate at any time."):
    present_alert(
        text,
        sub_message=sub_message,
        buttons=["OK"],
        wait=True,
        wait_seconds=900,
    )
    for _ in range(5):
        present_alert(
            text,
            sub_message=sub_message,
            buttons=["OK"],
            wait=False,
            wait_seconds=900,
        )
    sleep(9)
    present_alert(
        text,
        sub_message=sub_message,
        buttons=["OK"],
        wait=True,
        wait_seconds=900,
    )

# annoying_repeat("An unexpected error has occurred.")
