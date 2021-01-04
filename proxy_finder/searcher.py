"""
HttpSearcher tries random hosts for HTTP proxy services. It has the method
'search' that iterates proxies when they are found. The search process is
done in multiple threads.

Example:

    # Create a searcher with 100 threads
    searcher = HttpSearcher(100)

    # Search for 10 proxies and iterate them
    for proxy in searcher.search(10):
        print(proxy)
"""

import socket
from threading import Thread, Event
from queue import Queue
from random import randint, choice

import requests

from .proxy import Proxy


TRY_URL_DEFAULT = "http://example.com/"
CHECK_TIMEOUT_DEFAULT = 3.0


class HttpSearcher:
    # Ports list to search for proxies
    ports = (8080, 3128)

    def __init__(self, threads_num,
                 try_url=TRY_URL_DEFAULT,
                 check_timeout=CHECK_TIMEOUT_DEFAULT):
        self._threads_num = threads_num
        self._try_url = try_url
        self._check_timeout = check_timeout

    def search(self, count=None):
        """
        A generator that yields found proxies. 'count' is the number of proxies
        to find. If 'count' is None, the generator is infinite.
        """
        # Queue to fill proxies by threads
        queue = Queue()

        # Stop event for the threads
        stop_event = Event()

        # Threads to search for proxies
        threads = [
            Thread(target=self._find_target,
                             args=(queue, stop_event))
            for _ in range(self._threads_num)
        ]

        # Start threads
        list(map(Thread.start, threads))

        if count is not None:
            # Finite loop to search for proxies
            for _ in range(count):
                # Yield proxies that threads put into the queue
                yield queue.get(block=True)

            # Stop the threads by setting stop_event
            stop_event.set()

            # Wait until all threads are stopped
            list(map(Thread.join, threads))

        else:
            # Infinite loop to search for proxies
            while True:
                # Yield proxies that threads put into the queue
                yield queue.get(block=True)

    def _find_target(self, queue, stop_event):
        while not stop_event.is_set():
            proxy = self._get_random_proxy()
            if self._check_proxy(proxy):
                queue.put(proxy)

    def _get_random_proxy(self):
        host = ".".join(str(randint(0, 255)) for _ in range(4))
        port = choice(self.ports)
        return Proxy(host=host, port=port)

    def _check_proxy(self, proxy):
        return self._check_open_port(proxy) and self._try_proxy(proxy)

    def _check_open_port(self, proxy):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((proxy.host, proxy.port))
        sock.close()
        return result == 0

    def _try_proxy(self, proxy):
        proxies = {"http": f"http://{proxy.host}:{proxy.port}"}
        try:
            with requests.get(self._try_url, proxies=proxies,
                              timeout=self._check_timeout) as response:
                return response.status_code == 200
        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout) as exc:
            return False
