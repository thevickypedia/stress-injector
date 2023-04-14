import logging
import os
import platform
from enum import Enum
from typing import Callable

import requests

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


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


settings = Settings


class RequestType:
    """Wrapper for request types."""

    GET: Callable = requests.get
    PUT: Callable = requests.put
    POST: Callable = requests.post
    DELETE: Callable = requests.delete


_supported_systems = (operating_system.macOS, operating_system.linux, operating_system.windows)

if settings.os not in _supported_systems:
    raise UnsupportedOS(f"\n\ncurrently supported only on {', '.join(_supported_systems)}\n")
