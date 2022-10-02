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
    # midline
    for i in range(len(grid[0])):
        grid[int(len(grid)/2)+1][i] = "-"

    for h in grid:
        print("".join(h))

def audio_trace_init():
    # it will create a randomly oscillating image of sound
    # add horizontal columns which are -3 to +3 lines different from the previous one
    # assign variable for height and width
    max_height = os.get_terminal_size().lines
    max_width = os.get_terminal_size().columns
    grid = [[] for _ in range(max_height)]
    heightslist = []

    # initialize the 2d array with spaces
    for h in grid:
        for x in range(max_width):
            h.append(" ")

    height = 0
    for x in range(max_width):
        heightslist.append(0)

    grid = we_updating_da_grid(grid, heightslist)

    return grid, heightslist


def update_heights(grid, heightslist):

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

    return heightslist


def refresh_grid_and_view(grid, heightslist):
    clear_screen()
    print_grid(grid)
    heightslist = update_heights(grid, heightslist)
    grid = we_updating_da_grid(grid, heightslist)
