from multiprocessing import Process
from os import cpu_count
from sys import stdout
from threading import Thread
from time import sleep, time

from psutil import cpu_percent


class CPUStress:
    """`Controller <https://git.io/J9cXV>`__ for CPU stress using multiprocessing. Gets duration as user input.

    >>> CPUStress

    CPU is stressed using `multiprocessing.Process <https://docs.python.org/3/library/multiprocessing.html#
    the-process-class>`__ to run the infinite loop on each process.

    Args:
        seconds:
            - The number of seconds for which the CPU has to be stressed. Defaults to five times the number of cores.

    Warnings:
        - CPU stress is induced in real time.
        - A relatively low performing machine may stall when stress is induced for a long duration.

    References:
        >>> CPUStress._infinite()
            Triggers an infinite loop for the number of logical cores.

        >>> CPUStress._measure_cpu()
            Measures the impact on each logical core in a dedicated thread.
    """

    CORES = cpu_count()

    def __init__(self, seconds: int = CORES * 5):
        self.seconds = seconds
        self.start_time = None

    def _infinite(self) -> None:
        """Infinite loop to stress each core on the CPU for the number of logical cores available.

        See Also:
            The loop runs on each core as this function is triggered by ``processing.Process`` that runs as a loop.
        """
        while True:
            try:
                for _ in range(self.CORES):
                    pass
            except KeyboardInterrupt:
                return

    def _measure_cpu(self) -> None:
        r"""Uses ``cpu_percent()`` to get the current CPU utilization and print the utilization percentage on each core.

        Runs in a forever loop. Stops when the flag ``stop_thread`` is set to ``True``.
        """
        # noinspection PyGlobalUndefined
        global stop_thread
        processors = []
        while True:
            cpu_util = cpu_percent(interval=1, percpu=True)
            processors.append(cpu_util)  # stores the list of usage % as a list within a list
            output = ''
            for index, percent in enumerate(cpu_util):
                output += f'Core {index + 1}: {percent}%\t'
            stdout.write(f'\r{output.strip()}')
            if stop_thread:
                break
        stdout.write('\r')  # flushes the screen output
        processors = map(list, zip(*processors))
        processors = [max(processor) for processor in processors]
        processors = list(enumerate(processors))
        processors = sorted(processors, key=lambda x: x[1], reverse=True)

        if self.start_time and (run_time := round(time() - self.start_time)):
            if (stop_when := self.seconds - run_time) and stop_when > 0:
                print(f'Actual runtime: {run_time} seconds. Stopped {stop_when} seconds early.')
        else:
            print('Stress Test was stopped before it began.')

        print('CPU Usage Report:')
        [print(f'Core {processor + 1} - {self._format_number(usage)}%') for processor, usage in processors]

    @classmethod
    def _format_number(cls, n: float) -> int:
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
            infinite: To kick off stress injector.
            measure: To measure the usage in the background running in a dedicated thread.
        """
        # noinspection PyGlobalUndefined
        global stop_thread
        try:
            stdout.write(f'\rStressing CPU cores for {self.seconds} seconds')
            processes = []
            for n in range(self.CORES):
                processes.append(Process(target=self._infinite))
            stop_thread = False
            measure = Thread(target=self._measure_cpu)
            measure.start()
            sleep(1)
            self.start_time = time()
            [each_core.start() for each_core in processes]
            sleep(self.seconds)
            [each_core.terminate() for each_core in processes]
            [each_core.join() for each_core in processes]
            sleep(1)
            stop_thread = True
            measure.join()
        except KeyboardInterrupt:
            stdout.write('\rManual interrupt received. Stopping stress.')
            stop_thread = True


if __name__ == '__main__':
    CPUStress(seconds=60).run()
