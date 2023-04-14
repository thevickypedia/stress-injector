import logging
import time
import urllib.parse
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, NoReturn, Union

from .models import LOGGER, RequestType

RESULT = {'success': 0, 'errors': 0}


class URLStress:
    """Controller for URL stress using threadpool. Gets url as input.

    >>> URLStress

    """

    def __init__(self, url: str, rate: int = 1e+5, timeout: Union[int, float] = 5e-1,
                 retry_limit: Union[int, float] = 5, circuit_break: Union[int, float] = 5,
                 logger: logging.Logger = None, request_type: Callable = RequestType.GET,
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
        if self.parsed.scheme not in ('http', 'https', 'ws'):
            raise ValueError(
                f"\n\nbad url: {url}\n{self.parsed.scheme}"
            )
        self.LOGGER = logger or LOGGER
        self.request_url = url
        self.request_rate = int(rate)
        self.timeout = timeout
        self.retry_limit = retry_limit
        self.circuit_break = circuit_break
        self.kwargs = kwargs or {}
        self.request_type = request_type

    def make_request(self, sample: bool = False) -> NoReturn:
        """Makes a GET request to the endpoint.

        Args:
            sample: Boolean flag to indicate if the request is sample.
        """
        if sample:
            response = self.request_type(url=self.request_url, **self.kwargs)
        else:
            response = self.request_type(url=self.request_url, timeout=self.timeout, **self.kwargs)
        if response.ok:
            return
        else:
            response.raise_for_status()

    def initiate_injection(self) -> NoReturn:
        """Initiates injection in a thread pool."""
        futures = {}
        retries = 0
        executor = ThreadPoolExecutor(max_workers=self.request_rate)
        with executor:
            for iterator in range(1, int(self.request_rate) + 1):
                try:
                    future = executor.submit(self.make_request)
                except RuntimeError:
                    retries += 1
                    if retries > self.retry_limit:
                        self.LOGGER.error("Retry limit reached.")
                        break
                    self.LOGGER.warning("Hit rate limit. Awaiting 5 seconds before retry.")
                    time.sleep(self.circuit_break)
                    continue
                futures[future] = iterator
        for future in as_completed(futures):
            if future.exception():
                self.LOGGER.error(f'Thread processing for {iterator!r} received an exception: {future.exception()}')
                RESULT['errors'] += 1
            else:
                RESULT['success'] += 1

    def run(self) -> NoReturn:
        """Runs initiate request injection and prints success and error count."""
        try:
            self.make_request(sample=True)  # at least one request should pass before initiating request injection
        except Exception as error:
            warnings.warn(
                f"\n{error.__str__()}\n\ntest call failed, cannot proceed stress testing\n"
            )
            return
        self.LOGGER.info("Running request injection on '%s' with rate %s", self.parsed.netloc, f'{self.request_rate:,}')
        time.sleep(3)
        start = time.time()
        self.initiate_injection()
        self.LOGGER.info("Request injection completed in %f seconds", round(float(time.time() - start), 2))
        assert RESULT['success'] + RESULT['errors'] == self.request_rate, "Not all request trails were successful"
        self.LOGGER.info("Total number of requests passed: %d", RESULT['success'])
        self.LOGGER.warning("Total number of requests failed: %d", RESULT['errors'])


if __name__ == '__main__':
    injector = URLStress(url="http://0.0.0.0:5002")
    injector.run()
