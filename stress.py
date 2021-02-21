import os
import platform
import resource
import sys
import time
from multiprocessing import Process
from threading import Thread

import numpy
from psutil import cpu_percent, virtual_memory
from psutil import Process as Process_
from tqdm import tqdm

kill_signal = False


def stress(gb):
    """Generates random bytes with the multiple of 1024 (~1GB)"""
    mb2bytes = 1024 * 1024
    result = [numpy.random.bytes(mb2bytes) for _ in tqdm(range(gb), desc='Generating random bytes', unit=' bytes',
                                                         leave=False)]
    return f'Injected stress in bytes: {(len(result) * mb2bytes)}'


def memory_util_check():
    """Returns memory used only the current script."""
    operating_system = platform.system()
    if operating_system == 'Darwin':
        util = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return util
    elif operating_system == 'Windows':
        process = Process_(os.getpid())
        util = process.memory_info().peak_wset
        return util


def size_converter(byte_size):
    """Converts bytes into appropriate readable size."""
    import math
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    integer = int(math.floor(math.log(byte_size, 1024)))
    power = math.pow(1024, integer)
    size = round(byte_size / power, 2)
    response = str(size) + ' ' + size_name[integer]
    return response


def memory_stress():
    """Gets user input for the number of GBs stress has to be induced and triggers the memory stress"""
    current_memory = size_converter(virtual_memory().total)
    desired_bytes = input(f"Enter the number of GBs to stress your memory: "
                          f"(Optimal for you: {round(float(current_memory.split()[0]) * 5)} GB)\n")
    gigabytes = int(desired_bytes) * 1024  # gigabytes to megabytes
    try:
        print(f'Stressing Memory with {desired_bytes} GB')
        print(stress(gigabytes))
        print(size_converter(memory_util_check()))
    except KeyboardInterrupt:
        pass


def infinite():
    """Infinite loop to stress CPU"""
    while True:
        pass


def measure_cpu():
    """Uses cpu_percent to get the CPU utilization and prints the max impacted core"""
    max_percent, max_ = 0, ''
    while True:
        if kill_signal:
            break
        cpu_util = cpu_percent(interval=1, percpu=True)
        output = ''
        for index, percent in enumerate(cpu_util):
            output += f'Core {index + 1}: {percent}%\t'
            if max_percent < percent:
                max_percent = percent
                max_ = index + 1
        sys.stdout.write(f'\r{output.strip()}')
    print(f'\nMax induced stress: {int(max_percent)}% on Core {max_}')


def cpu_stress():
    """Initiates CPU stress using multiprocessing for the number of cores and
    CPU monitor using multiprocessing to notify CPU performance under stress."""
    global kill_signal
    waiter = int(input(f'Enter the number of seconds to stress your CPU cores: '
                       f'(Optimal for you: {os.cpu_count() * 5} secs)\n'))
    try:
        print(f'Stressing CPU cores for {waiter} seconds')
        processes = []
        for n in range(os.cpu_count()):
            processes.append(Process(target=infinite))
        measure = Thread(target=measure_cpu)
        [each_core.start() for each_core in processes]
        measure.start()
        time.sleep(waiter)
        [each_core.terminate() for each_core in processes]
        [each_core.join() for each_core in processes]
        time.sleep(2)
        kill_signal = True
        measure.join()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    memory_stress()
    cpu_stress()
