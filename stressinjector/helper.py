import os
import sys
from typing import Any, NoReturn

from .models import settings


def flush_screen() -> NoReturn:
    """Flushes the screen output.

    See Also:
        Writes new set of empty strings for the size of the terminal if ran using one.
    """
    if settings.interactive:
        sys.stdout.write(f"\r{' '.join(['' for _ in range(os.get_terminal_size().columns)])}")
    else:
        sys.stdout.write("\r")


def write_screen(text: Any) -> NoReturn:
    """Write text to a screen that can be cleared later.

    Args:
        text: Text to be written.
    """
    sys.stdout.write(f"\r{text}")
