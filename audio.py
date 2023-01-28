import os
import re
import subprocess

DEFAULT_VOICE = "Alex" # "Samantha" # Alex or Ava or Samantha or Daniel
SILENT_SONGS = False

def read_aloud(text, wait=False, no_numbers=True, voice=DEFAULT_VOICE, delay=0):
    # play with -r or --progress?
    if voice is None:
        voice = DEFAULT_VOICE

    if no_numbers:
        text = re.sub(r'\[[0123456789]+\]', '', text)

    text = re.sub(r'[\[\]=>\'\(\)]', '', text)
    text = text.replace("Cinco, Inc", "Cinco Inc")

    x = f"sleep {delay}; say '{text}'"
    if voice:
        x = x + f" -v {voice}"

    pro = subprocess.Popen([x], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    if wait:
        pro.wait()
    return pro

def play_dialup_sound():
    if SILENT_SONGS: return None
    pro = subprocess.Popen(["afplay dial_up_sound.mp3"], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    return pro

def play_reunited():
    if SILENT_SONGS: return None
    pro = subprocess.Popen(["afplay Reunited.mp3"], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    return pro

def play_acid_tunnel_of_love():
    if SILENT_SONGS: return None
    pro = subprocess.Popen(["afplay Acid_Tunnel_of_Love.mp3"], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    return pro
