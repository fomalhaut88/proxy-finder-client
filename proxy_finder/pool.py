from threading import Thread
from copy import copy
from queue import Queue, Empty
from random import choice, shuffle

import requests

from .proxy import Proxy
from . import utils


class PoolError(Exception):
    """
    Class for errors in Pool.
    """
    pass


class UnreachableInstanceError(PoolError):
    """
    Error for unreachable proxy-finder instance.
    """
    pass


class Pool:
    """
    Pool keeps a list of proxies and has some methods to work with them.
    """
    # Max number of threads used in Pool.request_many
    max_threads_default = 1000

    # Default timeout for one request in Pool.request.
    # To have a different timeout (including None) you should pass 'timeout'
    # explicitly as kwargs.
    timeout_default = 3.0

    def __init__(self, proxy_list, max_threads=max_threads_default):
        self._proxy_list = proxy_list
        self._max_threads = max_threads

    def __bool__(self):
        """
        Returns True if self._proxy_list is not empty, else False.
        """
        return bool(self._proxy_list)

    def __len__(self):
        """
        For len()
        """
        return len(self._proxy_list)

    def __iter__(self):
        """
        For use as an iterator.
        """
        yield from self._proxy_list

    def get_random(self):
        """
        Gets a random proxy object from the list.
        """
        return choice(self._proxy_list)

    def get_random_many(self, count):
        """
        Gets several number of proxy objects from the list. If 'count' is
        bigger than the number of proxies, all proxies will be returned in
        a random order.
        """
        proxy_list = copy(self._proxy_list)
        shuffle(proxy_list)
        return proxy_list[:count]

    def request(self, url, **kwargs):
        """
        Performs the request through a random proxy in the pool and repeats it
        in the loop with a different proxies if error happens.
        """
        # Set timeout
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout_default

        # Loop to request throught proxy
        while True:
            # Get random proxy from the pool
            proxy = self.get_random()

            try:
                # Try to request
                response = proxy.request(url, **kwargs)
            except (requests.exceptions.ProxyError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.SSLError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout):
                # Continue trying if error
                continue
            else:
                return response

    def request_many(self, args_list, **kwargs):
        """
        Requests URLs provided in args_list (with their custom parameters used
        in Proxy.request) parallelly using multi threading. 'kwargs' is common
        parameters (like headers, timeout, etc).
        """
        # Queues for input and output
        args_queue = utils.iter_to_queue(enumerate(args_list))
        result_queue = Queue()

        # Target for threads
        def target(args_queue, result_queue, kwargs, pool):
            while True:
                try:
                    idx, args = args_queue.get(block=False)
                except Empty:
                    break
                else:
                    response = pool.request(**args, **kwargs)
                    result_queue.put((idx, response))

        # Execute threads for shuffled proxies
        utils.execute_threads(
            Thread(target=target,
                   args=(args_queue, result_queue, kwargs, self))
            for _ in range(self._max_threads)
        )

        # Prepare result as list, None will be stored in case of error
        result_list = [None] * len(args_list)
        for idx, result in utils.queue_to_iter(result_queue):
            result_list[idx] = result
        return result_list

    def save(self, path):
        """
        Saves proxy list into a file.
        """
        with open(path, 'w') as f:
            for proxy in self._proxy_list:
                print(proxy, file=f)

    @classmethod
    def from_file(cls, path):
        """
        Loads pool from the given file.
        """
        with open(path) as f:
            proxy_list = [
                Proxy.from_str(line.strip())
                for line in f
            ]
        return cls(proxy_list)

    @classmethod
    def from_api(cls, api, options={}):
        """
        Loads pool from the API object with given options (that is passed to
        API.list).
        """
        try:
            result = api.list(options)['result']

        except requests.exceptions.ConnectTimeout:
            raise UnreachableInstanceError()

        else:
            proxy_list = [
                Proxy(**dct)
                for dct in result
            ]
            return cls(proxy_list)
