import os
import re
import subprocess
from utils import add_delay

q = "dall_e_image.png"

def present_image(image_fn, delay=0, wait=False):
    t = f"qlmanage -p {image_fn} -d 1"
    t = add_delay(t, delay)
    pro = subprocess.Popen([t], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
    if wait:
        pro.wait()

present_image(q)
