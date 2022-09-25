import os
import random
from utils import *
from time import sleep

# it will create a randomly oscillating image of sound
# add horizontal columns which are -3 to +3 lines different from the previous one
# assign variable for height and width
max_height = os.get_terminal_size().lines
max_width = os.get_terminal_size().columns
midpoint = max_height / 2
min_height = 0

l = [-3, -2, -1, 0, 1, 2, 3]

def audio_trace():
    # initialize the 2d array with dots
    twodarray = [[] for _ in range(max_height)]

    for h in twodarray:
        for x in range(max_width):
            h.append(" ")
        # print("".join(h))

    for i in range(max_width):
        twodarray[31][i] = "-"

    onedarray = []
    height = 0
    for x in range(max_width):
        randumb = random.choice(l)

        height = height + randumb
        if height > max_height:
            height = max_height
        if height < min_height:
            height = min_height
        # add height to array
        onedarray.append(height)

    # print(onedarray)
    # print("midpoint", midpoint)

    for h in range(max_height):
        for i in range(max_width):
            if abs(onedarray[i]) >= abs(midpoint - h):
                twodarray[h][i] = "-"

    for h in twodarray:
        print("".join(h))

while True:
    clear_screen()
    audio_trace()
    sleep(0.5)
