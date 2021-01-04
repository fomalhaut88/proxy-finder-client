"""
Some utils used in the library.
"""

from queue import Queue
from threading import Thread


def iter_to_queue(itr):
    """
    Creates queue from the iterator.
    """
    queue = Queue()
    for item in itr:
        queue.put(item)
    return queue


def queue_to_iter(queue):
    """
    Iterates the queue.
    """
    while not queue.empty():
        yield queue.get(block=False)


def execute_threads(threads_gen):
    """
    Starts and executed the threads passed as generator.
    """
    threads = list(threads_gen)
    list(map(Thread.start, threads))
    list(map(Thread.join, threads))
