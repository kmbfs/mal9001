from time import sleep
import psutil

def kill_noise_processes():
    for process_type, process_ids in check_current_processes().items():
        if process_type in ["afplay", "say"]:
            for id in process_ids:
                pro = psutil.Process(id)
                pro.kill()

def check_current_processes(verbose=False):
    process_types = {
        "afplay":[],
        "python3.7":[],
        "say":[],
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
