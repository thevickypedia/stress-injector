import logging
import math
import time
from typing import Union

import psutil
from numpy.random import bytes
from tqdm import tqdm

from .helper import flush_screen
from .models import LOGGER, operating_system, settings

if settings.os != operating_system.windows:
    import resource


def _size_converter(byte_size: Union[int, float]) -> str:
    """Gets the current memory consumed and converts it to human friendly format.

    Args:
        byte_size: Receives byte size as argument.

    Returns:
        str:
        Converted human understandable size.
    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    integer = int(math.floor(math.log(byte_size, 1024)))
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

    MAX_DEFAULT = round(float(_size_converter(psutil.virtual_memory().total).split()[0]) * 2)

    def __init__(self, gigabytes: int = MAX_DEFAULT, logger: logging.Logger = None):
        """Instantiates the members of the class.

        Args:
            gigabytes: The number of gigabytes, memory has to be stressed. Defaults to twice the physical memory.
            logger: Custom logger.
        """
        self.LOGGER = logger or LOGGER
        self.gigabytes = gigabytes
        self._run()

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
        result = [bytes(mb2bytes) for _ in tqdm(range(mb), desc='Generating random bytes', unit=' bytes', leave=False)]
        return f'Stress Injected: {_size_converter(len(result) * mb2bytes)}'

    @classmethod
    def _memory_util_check(cls) -> Union[int, float]:
        """Returns memory used only the current script.

        Returns:
            int or float:
            The memory used by the current process.

        References:
            **macOS or Linux:**
                - https://man7.org/linux/man-pages/man2/getrusage.2.html#:~:text=RUSAGE_CHILDREN

                >>> resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

                `getrusage <https://docs.python.org/3/library/resource.html#resource.getrusage>`__

            **Windows:**
                >>> psutil.Process(settings.pid).memory_info().peak_wset

                `memory_info <https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info>`__
        """
        if settings.os == operating_system.macOS:
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if settings.os == operating_system.linux:
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1e+3
        if settings.os == operating_system.windows:
            return psutil.Process(settings.pid).memory_info().peak_wset

    def _run(self) -> None:
        """Initiator for stress injector. Converts GigaBytes to Bytes.

        Methods:
            stress: To kick off stress injector with the desired bytes converted from user input.
            memory_util_check: To measure the usage post completion.
        """
        megabytes = int(self.gigabytes) * 1024  # gigabytes to megabytes
        try:
            self.LOGGER.info('Stressing Memory with %d GB', self.gigabytes)
            time.sleep(1)
            flush_screen()
            self.LOGGER.info(self._stress(mb=megabytes) + '\n')
        except KeyboardInterrupt:
            self.LOGGER.warning('Manual interrupt received. Stopping stress.')
            time.sleep(1)
            flush_screen()
        self.LOGGER.info('Actual memory Consumed: %s', _size_converter(self._memory_util_check()))
