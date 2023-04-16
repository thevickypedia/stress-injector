import logging
import os
import platform
import sys
from enum import Enum

LOGGER = logging.getLogger(__name__)
DEFAULT_LOG_FORM = '%(asctime)s - %(levelname)s - [%(processName)s:%(module)s:%(lineno)d] - %(funcName)s - %(message)s'
DEFAULT_FORMATTER = logging.Formatter(datefmt='%b-%d-%Y %I:%M:%S %p', fmt=DEFAULT_LOG_FORM)
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(fmt=DEFAULT_FORMATTER)
LOGGER.addHandler(hdlr=HANDLER)
LOGGER.setLevel(level=logging.DEBUG)


class UnsupportedOS(OSError):
    """Custom OSError for unsupported operating system."""


class OperatingSystem(str, Enum):
    """Wrapper for supported operating systems."""

    macOS: str = "Darwin"
    linux: str = "Linux"
    windows: str = "Windows"


operating_system = OperatingSystem


class Settings:
    """Wrapper for settings."""

    pid: int = os.getpid()
    os: str = platform.system()
    if sys.stdin.isatty():
        interactive = True
    else:
        interactive = False


settings = Settings


class RequestType(str, Enum):
    """Wrapper for request types."""

    get: str = "get"
    put: str = "put"
    post: str = "post"
    delete: str = "delete"


_supported_systems = (operating_system.macOS, operating_system.linux, operating_system.windows)

if settings.os not in _supported_systems:
    raise UnsupportedOS(f"\n\ncurrently supported only on {', '.join(_supported_systems)}\n")
