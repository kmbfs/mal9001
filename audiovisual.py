import sys
import os
import random
from utils import *
from time import sleep

RANDOM_SHIFTS = [-3, -2, -1, 0, 1, 2]

def we_updating_da_grid(grid, heightslist):
    for h in range(len(grid)):
        for i in range(len(heightslist)):
            if abs(heightslist[i]) >= abs((len(grid)/2) - h):
                grid[h][i] = "-"
            else:
                grid[h][i] = " "

    return grid

def print_grid(grid):
    for h in grid:
        print("".join(h))

def audio_trace_init():

    # it will create a randomly oscillating image of sound
    # add horizontal columns which are -3 to +3 lines different from the previous one
    # assign variable for height and width
    max_height = os.get_terminal_size().lines
    max_width = os.get_terminal_size().columns
    midpoint = max_height / 2
    min_height = 0
    grid = [[] for _ in range(max_height)]
    heightslist = []

    # initialize the 2d array with dots

    for h in grid:
        for x in range(max_width):
            h.append(" ")
        print("".join(h))

    for i in range(max_width):
        grid[31][i] = "-"


    height = 0
    for x in range(max_width):
        randumb = random.choice(RANDOM_SHIFTS)

        height = height + randumb
        if height > max_height / 2:
            height = max_height / 2
        if height < 0:
            height = 0
        # add height to array
        heightslist.append(height)

    # print(heightslist)
    # print("midpoint", midpoint)
    grid = we_updating_da_grid(grid, heightslist)

    print_grid(grid)

    return grid, heightslist


def update_heights(grid, heightslist):

    print('before', heightslist)

    for i in range(len(heightslist)):
        if i == len(heightslist) - 1:
            height = heightslist[i - 1] + random.choice(RANDOM_SHIFTS)

            if height > len(grid) / 2:
                height = len(grid) / 2
            if height < 0:
                height = 0

            heightslist[i] = height
        else:
            heightslist[i] = heightslist[i + 1]

    print('after', heightslist)
    return heightslist

grid, heightslist = audio_trace_init()
while True:
    clear_screen()
    print_grid(grid)
    heightslist = update_heights(grid, heightslist)
    grid = we_updating_da_grid(grid, heightslist)
    sleep(0.01)
