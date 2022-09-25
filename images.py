import os
import re
import subprocess
from utils import add_delay

DALL_E_IMAGE_FN = "dall_e_image.png"

def present_image(image_fn, delay=0, wait=False):
    t = f"qlmanage -p {image_fn} -d 0"
    t = add_delay(t, delay)
    pro = subprocess.Popen([t], stdout=None,
                           shell=True)
    if wait:
        pro.wait()

# present_image(DALL_E_IMAGE_FN)
