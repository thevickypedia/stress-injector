from math import floor, log, pow
from os import getpid
from platform import system
from resource import RUSAGE_SELF, getrusage

from numpy.random import bytes
from psutil import Process, virtual_memory
from tqdm import tqdm


class MemoryStress:
    """`Controller <https://git.io/JW70h>`__ to trigger the memory stress. Gets number of GBs as user input.

    >>> MemoryStress

    Args:
        gigabytes: [Optional] The number of gigabytes for which the memory has to be stressed.
            If no value is provided, there will be a prompt to enter an integer value.

    See Also:
        Suggests twice the amount of physical memory.

    Warnings:
        - DO heed the optimal value suggested before entering the input GB value.
        - Memory stress is induced in real time.
        - A low RAM equipped machine may stall or be un-responsive when stress is induced for a higher byte value.

    References:
        >>> MemoryStress.stress()
            Generates ``random bytes``, 1024 times the ``GigaBytes`` value entered during prompt or class intialization.

        >>> MemoryStress.size_converter()
            Converts bytes to human readable size format.
    """
    def __init__(self, gigabytes: int = None):
        current_memory = self.size_converter(virtual_memory().total)
        if gigabytes:
            self.gigabytes = gigabytes
        else:
            self.gigabytes = int(input(f"Enter the number of GBs to stress your memory: "
                                       f"(Optimal for you: {round(float(current_memory.split()[0]) * 2)} GB)\n"))

    def stress(self, mb) -> str:
        """Generates `random bytes <https://numpy.org/doc/stable/reference/random/generated/numpy.random.bytes.html>`__.

        Bytes are generated with the multiple of 1024 ~ 1GB. Uses tqdm module to show a progress bar.

        Args:
            mb: The number of ``MegaBytes`` of stress has be induced A.k.a random bytes have to be generated.

        Returns:
            str:
            Calls the ``size_converter`` method to get the human readable size of stress that was induced.
        """
        mb2bytes = 1024 * 1024
        result = [bytes(mb2bytes) for _ in tqdm(range(mb), desc='Generating random bytes', unit=' bytes',
                                                leave=False)]
        return f'Stress Injected: {self.size_converter(len(result) * mb2bytes)}'

    @classmethod
    def memory_util_check(cls) -> int:
        """Returns memory used only the current script.

        Returns:
            int:
            The memory used by the current process.

        References:
            MacOS:
                >>> getrusage(RUSAGE_SELF).ru_maxrss
                    `getrusage <https://docs.python.org/3/library/resource.html#resource.getrusage>`__

            Windows:
                >>> process.memory_info().peak_wset
        """
        operating_system = system()
        if operating_system == 'Darwin':
            return getrusage(RUSAGE_SELF).ru_maxrss
        elif operating_system == 'Windows':
            process = Process(getpid())
            return process.memory_info().peak_wset

    @classmethod
    def size_converter(cls, byte_size) -> str:
        """Gets the current memory consumed and converts it to human friendly format.

        Args:
            byte_size: Receives byte size as argument.

        Returns:
            str:
            Converted human understandable size.
        """
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        integer = int(floor(log(byte_size, 1024)))
        power = pow(1024, integer)
        size = round(byte_size / power, 2)
        response = str(size) + ' ' + size_name[integer]
        return response

    def run(self):
        """Initiator for stress injector. Converts GigaBytes to Bytes.

        Methods:
            - stress: To kick off stress injector with the desired bytes converted from user input.
            - memory_util_check: To measure the usage post completion.
        """
        megabytes = int(self.gigabytes) * 1024  # gigabytes to megabytes
        try:
            print(f'Stressing Memory with {self.gigabytes} GB')
            print(self.stress(mb=megabytes))
            print(f'Memory Consumed: {self.size_converter(self.memory_util_check())}')
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    MemoryStress(gigabytes=10).run()
