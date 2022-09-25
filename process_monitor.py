from utils import *
from display import *
from check_processes import *

def continuous_process_monitor(refresh_secs=1):
    while True:
        sleep(refresh_secs)
        pros = check_current_processes()
        has_noise = False

        for p,pids in pros.items():
            if len(pids) == 0: continue
            if p in NOISE_PROCESSES:
                clear_screen()
                matrix_fill()
                has_noise = True

        if not has_noise:
            clear_screen()

continuous_process_monitor(refresh_secs=0.5)
