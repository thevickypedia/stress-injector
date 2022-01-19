from math import floor, log, pow
from os import getpid
from platform import system
from resource import RUSAGE_SELF, getrusage
from sys import stdout
from time import sleep
from typing import Union

from numpy.random import bytes
from psutil import Process, virtual_memory
from tqdm import tqdm


def _size_converter(byte_size: Union[int, float]) -> str:
    """Gets the current memory consumed and converts it to human friendly format.

    Args:
        byte_size: Receives byte size as argument.

    Returns:
        str:
        Converted human understandable size.
    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    integer = int(floor(log(byte_size, 1024)))
    size = round(byte_size / pow(1024, integer), 2)
    return str(size) + ' ' + size_name[integer]


class MemoryStress:
    """`Controller <https://git.io/J9cXr>`__ to trigger the memory stress. Gets number of GBs as user input.

    >>> MemoryStress

    Args:
        gigabytes:
            - The number of gigabytes for which the memory has to be stressed. Defaults to twice the number of GBs.

    See Also:
        Suggests twice the amount of physical memory.

    Warnings:
        - Memory stress is induced in real time.
        - A low RAM equipped machine may stall or be un-responsive when stress is induced for a higher byte value.

    References:
        >>> MemoryStress._stress()

            Generates ``random bytes``, 1024 times the ``GigaBytes`` value entered during prompt or class intialization.

        >>> _size_converter()

            Converts ``bytes`` to human-readable size format.
    """

    MAX_DEFAULT = round(float(_size_converter(virtual_memory().total).split()[0]) * 2)

    def __init__(self, gigabytes: int = MAX_DEFAULT):
        self.gigabytes = gigabytes

    @classmethod
    def _stress(cls, mb: int) -> str:
        """Generates `random bytes <https://numpy.org/doc/stable/reference/random/generated/numpy.random.bytes.html>`__.

        Bytes are generated with the multiple of 1024 ~ 1GB. Uses tqdm module to show a progress bar.

        Args:
            mb: The number of ``MegaBytes`` of stress has be induced A.k.a. random bytes have to be generated.

        Returns:
            str:
            Calls the ``size_converter`` method to get the human-readable size of stress that was induced.
        """
        mb2bytes = 1024 * 1024
        result = [bytes(mb2bytes) for _ in tqdm(range(mb), desc='Generating random bytes', unit=' bytes',
                                                leave=False)]
        return f'Stress Injected: {_size_converter(len(result) * mb2bytes)}'

    @classmethod
    def _memory_util_check(cls) -> int:
        """Returns memory used only the current script.

        Returns:
            int:
            The memory used by the current process.

        References:
            **MacOS:**
                >>> getrusage(RUSAGE_SELF).ru_maxrss

                `getrusage <https://docs.python.org/3/library/resource.html#resource.getrusage>`__

            **Windows:**
                >>> process.memory_info().peak_wset

                `memory_info <https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info>`__
        """
        operating_system = system()
        if operating_system == 'Darwin':
            return getrusage(RUSAGE_SELF).ru_maxrss
        elif operating_system == 'Windows':
            process = Process(getpid())
            return process.memory_info().peak_wset

    def run(self) -> None:
        """Initiator for stress injector. Converts GigaBytes to Bytes.

        Methods:
            stress: To kick off stress injector with the desired bytes converted from user input.
            memory_util_check: To measure the usage post completion.
        """
        megabytes = int(self.gigabytes) * 1024  # gigabytes to megabytes
        try:
            stdout.write(f'\rStressing Memory with {self.gigabytes} GB')
            sleep(1)
            stdout.write(self._stress(mb=megabytes) + '\n')
        except KeyboardInterrupt:
            stdout.write('\rManual interrupt received. Stopping stress.\n')
            sleep(1)
        print(f'Actual memory Consumed: {_size_converter(self._memory_util_check())}')


if __name__ == '__main__':
    MemoryStress(gigabytes=1).run()
