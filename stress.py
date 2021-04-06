import sys
from math import log, floor, pow
from multiprocessing import Process as Multiprocess
from os import getpid, cpu_count
from platform import system
from resource import getrusage, RUSAGE_SELF
from threading import Thread
from time import sleep

from numpy.random import bytes
from psutil import cpu_percent, virtual_memory, Process
from tqdm import tqdm

kill_signal = False


def stress(gb):
    """Generates random bytes with the multiple of 1024 (~1GB)"""
    mb2bytes = 1024 * 1024
    result = [bytes(mb2bytes) for _ in tqdm(range(gb), desc='Generating random bytes', unit=' bytes',
                                            leave=False)]
    return f'Stress Injected: {size_converter(len(result) * mb2bytes)}'


def memory_util_check():
    """Returns memory used only the current script."""
    operating_system = system()
    if operating_system == 'Darwin':
        return getrusage(RUSAGE_SELF).ru_maxrss
    elif operating_system == 'Windows':
        process = Process(getpid())
        return process.memory_info().peak_wset


def size_converter(byte_size):
    """Converts bytes into appropriate readable size."""
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    integer = int(floor(log(byte_size, 1024)))
    power = pow(1024, integer)
    size = round(byte_size / power, 2)
    response = str(size) + ' ' + size_name[integer]
    return response


def memory_stress():
    """Gets user input for the number of GBs stress has to be induced and triggers the memory stress.
    Suggests twice the amount of physical memory."""
    current_memory = size_converter(virtual_memory().total)
    desired_bytes = input(f"Enter the number of GBs to stress your memory: "
                          f"(Optimal for you: {round(float(current_memory.split()[0]) * 2)} GB)\n")
    gigabytes = int(desired_bytes) * 1024  # gigabytes to megabytes
    try:
        print(f'Stressing Memory with {desired_bytes} GB')
        print(stress(gigabytes))
        print(f'Memory Consumed: {size_converter(memory_util_check())}')
    except KeyboardInterrupt:
        pass


def infinite():
    """Infinite loop to stress CPU"""
    while True:
        try:
            for _ in range(cpu_count()):
                pass
        except KeyboardInterrupt:
            sys.exit(0)


def measure_cpu():
    """Uses cpu_percent to get the CPU utilization and prints the max impacted core"""
    processors = []
    while True:
        if kill_signal:
            break
        cpu_util = cpu_percent(interval=1, percpu=True)
        processors.append(cpu_util)  # stores the list of usage % as a list within a list
        output = ''
        for index, percent in enumerate(cpu_util):
            output += f'Core {index + 1}: {percent}%\t'
        sys.stdout.write(f'\r{output.strip()}')
    sys.stdout.write('\r')  # flushes the screen output
    processors = map(list, zip(*processors))  # transpose matrix, so first list will have all usage % of core1 and so on
    processors = [max(processor) for processor in processors]  # gets the maximum of each list to convert matrix to list
    processors = list(enumerate(processors))  # creates a list of index values and CPU usage in a set
    processors = sorted(processors, key=lambda x: x[1], reverse=True)  # sorts by CPU usage within the set in the list

    def format_number(n):
        """Converts numbers with float value .0 to integers"""
        return int(n) if isinstance(n, float) and n.is_integer() else n

    print('CPU Usage:')
    [print(f'Core {processor + 1} - {format_number(usage)}%') for processor, usage in processors]


def cpu_stress():
    """Initiates CPU stress using multiprocessing for the number of cores and
    CPU monitor using multiprocessing to notify CPU performance under stress."""
    global kill_signal
    waiter = int(input(f'Enter the number of seconds to stress your CPU cores: '
                       f'(Optimal for you: {cpu_count() * 5} secs)\n'))
    try:
        print(f'Stressing CPU cores for {waiter} seconds')
        processes = []
        for n in range(cpu_count()):
            processes.append(Multiprocess(target=infinite))
        measure = Thread(target=measure_cpu)
        [each_core.start() for each_core in processes]
        measure.start()
        sleep(waiter)
        [each_core.terminate() for each_core in processes]
        [each_core.join() for each_core in processes]
        sleep(2)
        kill_signal = True
        measure.join()
    except KeyboardInterrupt:
        kill_signal = True


if __name__ == '__main__':
    memory_stress()
    cpu_stress()
