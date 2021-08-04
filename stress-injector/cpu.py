import sys
from multiprocessing import Process
from os import cpu_count
from threading import Thread
from time import sleep

from psutil import cpu_percent

kill_signal = False


def infinite() -> None:
    """Infinite loop to stress each core on the CPU for the number of logical cores available.

    See Also:
        The loop runs on each core as this function is triggered by `processing.Process` which itself runs as a loop.
    """
    while True:
        try:
            for _ in range(cpu_count()):
                pass
        except KeyboardInterrupt:
            sys.exit(0)


def measure_cpu() -> None:
    r"""Uses `cpu_percent()` to get the current CPU utilization and prints the utilization percentage on each core.

    Runs until the global variable `kill_signal` is set to True.

    See Also:
        - The `stdout` is set to write and flush as the % value changes.
        - This is done using the `sys.stdout.write` module which is set to work as expected only in an IDE.
        - Sorry Terminal fans, but on the bright side,
          `os.system('clear')` can be added right after `sys.stdout.write(f'\\r{output.strip()}')`
    """
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

    print('CPU Usage:')
    [print(f'Core {processor + 1} - {format_number(usage)}%') for processor, usage in processors]


def format_number(n) -> int:
    """Converts numbers with float value .0 to integers.

    Args:
        n: Raw numbers which is either a `str` or `float`

    Returns:
        int:
        Processed integers without any float value extensions in it.
    """
    return int(n) if isinstance(n, float) and n.is_integer() else n


def cpu_stress() -> None:
    """`Controller <https://git.io/JW70u>`__ for CPU stress using multiprocessing. Gets duration as user input.

    CPU is stressed using `multiprocessing.Process <https://docs.python.org/3/library/multiprocessing.html#
    the-process-class>`__ to run the infinite loop on each process.

    See Also:
        Suggests a duration (in seconds) that is 5 times the # of logical cores present.

    Warnings:
        - DO heed the optimal value suggested before entering the input duration.
        - CPU stress is induced in real time.
        - A relatively low performing machine may stall or be un-responsive when stress is induced for a long duration.

    References:
        >>> infinite()
            Triggers an infinite loop for the number of logical cores.
        >>> measure_cpu()
            Measures the impact on each logical core in a dedicated thread.
    """
    global kill_signal
    waiter = int(input(f'Enter the number of seconds to stress your CPU cores: '
                       f'(Optimal for you: {cpu_count() * 5} secs)\n'))
    try:
        print(f'Stressing CPU cores for {waiter} seconds')
        processes = []
        for n in range(cpu_count()):
            processes.append(Process(target=infinite))
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
    cpu_stress()
