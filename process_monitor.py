from utils import *
from display import *
from check_processes import *
from audiovisual import refresh_grid_and_view, audio_trace_init

def continuous_process_monitor(refresh_secs=1):
    grid, heightslist = audio_trace_init()

    while True:
        sleep(refresh_secs)
        pros = check_current_processes()
        has_noise = False

        for p, pids in pros.items():
            if len(pids) != 0 and p in NOISE_PROCESSES:
                has_noise = True

        if has_noise:
            refresh_grid_and_view(grid, heightslist)

        if not has_noise:
            grid, heightslist = audio_trace_init()
            clear_screen()

continuous_process_monitor(refresh_secs=0.002)
