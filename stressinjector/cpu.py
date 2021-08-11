import sys
from multiprocessing import Process
from os import cpu_count
from threading import Thread
from time import sleep, time

from psutil import cpu_percent


class CPUStress:
    """`Controller <https://git.io/JW70u>`__ for CPU stress using multiprocessing. Gets duration as user input.

    >>> CPUStress

    CPU is stressed using `multiprocessing.Process <https://docs.python.org/3/library/multiprocessing.html#
    the-process-class>`__ to run the infinite loop on each process.

    Args:
        seconds: [Optional] The number of seconds for which the logical cores have to be stressed.
            If no value is provided, there will be a prompt to enter an integer value.

    See Also:
        Suggests a duration (in seconds) that is 5 times the number of logical cores present.

    Warnings:
        - DO heed the optimal value suggested before entering the input duration.
        - CPU stress is induced in real time.
        - A relatively low performing machine may stall when stress is induced for a long duration.

    References:
        >>> CPUStress.infinite()
            Triggers an infinite loop for the number of logical cores.

        >>> CPUStress.measure_cpu()
            Measures the impact on each logical core in a dedicated thread.
    """
    def __init__(self, seconds: int = None):
        self.cores = cpu_count()
        if seconds:
            self.seconds = seconds
        else:
            self.seconds = int(input(f'Enter the number of seconds to stress your CPU cores: '
                                     f'(Optimal for you: {self.cores * 5} secs)\n'))

    def infinite(self) -> None:
        """Infinite loop to stress each core on the CPU for the number of logical cores available.

        See Also:
            The loop runs on each core as this function is triggered by ``processing.Process`` that runs as a loop.
        """
        while True:
            try:
                for _ in range(self.cores):
                    pass
            except KeyboardInterrupt:
                sys.exit(0)

    def measure_cpu(self) -> None:
        r"""Uses `cpu_percent()` to get the current CPU utilization and prints the utilization percentage on each core.

        Runs until the current time reaches 3 seconds in addition to the user input.

        See Also:
            - The `stdout` is set to write and flush as the % value changes.
            - This is done using the ``sys.stdout.write`` module which is set to work as expected only in an IDE.
            - Sorry Terminal fans, but on the bright side,
              ``os.system('clear')`` can be added right after ``sys.stdout.write(f'\\r{output.strip()}')``
            - Uses transpose matrix, so first list will have all usage % of core1 and so on.
            - Gets the maximum of each list to convert matrix to list.
            - Creates a list of index values and CPU usage in a set.
            - Sorts by CPU usage within the set in the list.
        """
        end_time = time() + self.seconds + 3
        processors = []
        while time() <= end_time:
            cpu_util = cpu_percent(interval=1, percpu=True)
            processors.append(cpu_util)  # stores the list of usage % as a list within a list
            output = ''
            for index, percent in enumerate(cpu_util):
                output += f'Core {index + 1}: {percent}%\t'
            sys.stdout.write(f'\r{output.strip()}')
        sys.stdout.write('\r')  # flushes the screen output
        processors = map(list, zip(*processors))
        processors = [max(processor) for processor in processors]
        processors = list(enumerate(processors))
        processors = sorted(processors, key=lambda x: x[1], reverse=True)

        print('CPU Usage:')
        [print(f'Core {processor + 1} - {self.format_number(usage)}%') for processor, usage in processors]

    @classmethod
    def format_number(cls, n) -> int:
        """Converts numbers with float value .0 to integers.

        Args:
            n: Raw numbers which is either a `str` or `float`

        Returns:
            int:
            Processed integers without any float value extensions in it.
        """
        return int(n) if isinstance(n, float) and n.is_integer() else n

    def run(self) -> None:
        """Initiator for stress injector.

        Methods:
            - infinite: To kick off stress injector.
            - measure: To measure the usage in the background running in a dedicated thread.
        """
        try:
            print(f'Stressing CPU cores for {self.seconds} seconds')
            processes = []
            for n in range(self.cores):
                processes.append(Process(target=self.infinite))
            measure = Thread(target=self.measure_cpu)
            [each_core.start() for each_core in processes]
            measure.start()
            sleep(self.seconds)
            [each_core.terminate() for each_core in processes]
            [each_core.join() for each_core in processes]
            sleep(2)
            measure.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    CPUStress(seconds=60).run()
