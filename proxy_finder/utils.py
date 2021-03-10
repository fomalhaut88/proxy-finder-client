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


def prepare_list_params(options):
    params = {}
    dict_pass_value(options, params, 'country')
    dict_pass_value(options, params, 'region')
    dict_pass_value(options, params, 'city')
    dict_pass_value(options, params, 'count', str)
    dict_pass_value(options, params, 'score', str)
    dict_pass_value(options, params, 'ordered',
                          lambda x: '1' if x else '')
    dict_pass_value(options, params, 'format')
    return params


def dict_pass_value(src_dict, dst_dict, key, modifier=None):
    if modifier is None:
        modifier = lambda x: x
    if key in src_dict:
        dst_dict[key] = modifier(src_dict[key])
