from time import sleep
import psutil
from utils import clear_screen

NOISE_PROCESSES = ["afplay", "say"]
COMMAND_PROCESSES = ["python3.7"]

def kill_noise_processes():
    for process_type, process_ids in check_current_processes().items():
        if process_type in NOISE_PROCESSES:
            for id in process_ids:
                pro = psutil.Process(id)
                pro.kill()

def check_current_processes(verbose=False):
    process_types = {
        p:[]
        for p in NOISE_PROCESSES+COMMAND_PROCESSES
    }
    for process in psutil.process_iter():
        with process.oneshot():
            if process.name() in process_types.keys():
                process_types[process.name()].append(process.pid)
                # print(process.children(recursive=True))
    if verbose: print(process_types)
    return process_types

def continuous_check(verbose=False):
    while True:
        check_current_processes(verbose=verbose)
        sleep(1)
