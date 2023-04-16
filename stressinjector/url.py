import logging
import time
import urllib.parse
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
from typing import NoReturn, Union

import requests

from .models import LOGGER, RequestType


class URLStress:
    """Controller for URL stress using threadpool. Gets url as input.

    >>> URLStress

    """

    RESULT = {'success': 0, 'errors': 0}
    EVENT = Event()

    def __init__(self, url: str, rate: int = 1e+5, timeout: Union[int, float] = None,
                 logger: logging.Logger = None, request_type: str = RequestType.get,
                 **kwargs):
        """Instantiate the object, parse and validate the URL.

        Args:
            url: URL to inject stress.
            rate: Number of calls to make.
            timeout: Timeout for each request.
            retry_limit: Retry limit if the system is unable to spinup more threads.
            circuit_break: Wait time in seconds between retries.
            logger: Custom logger.
            request_type: Function from ``requests`` module.
            kwargs: Keyword arguments to use in the request.
        """
        self.parsed = urllib.parse.urlparse(url=url, allow_fragments=True)
        if self.parsed.scheme not in ('http', 'https', 'ws', 'ftp', 'tcp', 'udp', 'ssh',
                                      'gopher', 'mailto', 'news', 'telnet', 'file', 'nntp', 'wais'):
            raise ValueError(
                f"\n\nbad url: {url}\n{self.parsed.scheme}"
            )
        if request_type not in RequestType.__members__.keys():
            raise ValueError(
                f"\n\nbad request type: {request_type}\n\nallowed: {', '.join(RequestType.__members__.keys())}"
            )
        self.LOGGER = logger or LOGGER
        self.request_url = url
        self.request_rate = int(rate)
        self.timeout = timeout
        self.kwargs = kwargs or {}
        self.request_type = request_type
        self._run()

    def make_request(self, sample: bool = False) -> NoReturn:
        """Makes a GET request to the endpoint.

        Args:
            sample: Boolean flag to indicate if the request is sample.
        """
        if self.EVENT.is_set():
            return
        if sample:
            response = requests.request(method=self.request_type.lower(), url=self.request_url, **self.kwargs)
        else:
            response = requests.request(method=self.request_type.lower(), url=self.request_url,
                                        timeout=self.timeout, **self.kwargs)
        if response.ok:
            return
        else:
            response.raise_for_status()

    def initiate_injection(self) -> bool:
        """Initiates injection in a thread pool.

        Returns:
            bool:
            Returns a boolean flag based on successful completion.
        """
        futures = {}
        executor = ThreadPoolExecutor(max_workers=self.request_rate)
        with executor:
            for iterator in range(1, int(self.request_rate) + 1):
                try:
                    future = executor.submit(self.make_request)
                    futures[future] = iterator
                except RuntimeError as error:
                    self.LOGGER.error(error)
                    self.LOGGER.warning("cancelling future tasks")
                    future.cancel()
                    self.EVENT.set()
                    total = len(futures)
                    returned = sum(self.RESULT.values())
                    self.LOGGER.warning("calls made: %d", f'{total:,}')
                    self.LOGGER.warning("calls completed: %d", f'{returned:,}')
                    self.LOGGER.warning("calls pending: %d", f'{total - returned:,}')
                    self.LOGGER.warning("awaiting pending tasks to complete")
                    return False
        for future in as_completed(futures):
            if future.exception():
                self.LOGGER.error("thread processing for '%s' received an exception: '%s'",
                                  iterator, future.exception())
                self.RESULT['errors'] += 1
            else:
                self.RESULT['success'] += 1
        return True

    def _run(self) -> NoReturn:
        """Runs initiate request injection and prints success and error count."""
        try:
            self.LOGGER.info("Initiating sample call")
            self.make_request(sample=True)  # at least one request should pass before initiating request injection
            self.LOGGER.info("Sample call successful")
        except Exception as error:
            warnings.warn(
                f"\n{error.__str__()}\n\ntest call failed, cannot proceed stress testing\n"
            )
            return
        self.LOGGER.info("Running request injection on '%s' with rate %s", self.parsed.netloc, f'{self.request_rate:,}')
        start = time.time()
        run_assert = self.initiate_injection()
        self.LOGGER.info("Request injection completed in %f seconds", round(float(time.time() - start), 2))
        self.LOGGER.info("Total number of requests passed: %d", self.RESULT['success'])
        self.LOGGER.warning("Total number of requests failed: %d", self.RESULT['errors'])
        if run_assert:
            assert sum(self.RESULT.values()) == self.request_rate, "Not all request trails were successful"
        else:
            self.LOGGER.warning("Total number of requests abandoned: %d", self.request_rate - sum(self.RESULT.values()))
