"""

Measures on 8 core AMD cpu:

**proper coming up, previous one were shit**


"""


SKIP_MULTIPROCESSING = False


try:
    from multiprocessing import Process
except ImportError:
    Process = None
    SKIP_MULTIPROCESSING = True
import time
from threading import Thread


def timeit(method):
    """
    Thanks John! http://stackoverflow.com/a/2662229/294579
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec\n' % (method.__name__, args, kw, te-ts))
        return result
    return timed


def countdown(n):
    if n <= 0:
        return
    while n > 0:
        n -= 1


# @timeit
def countdown_linear(n):
    countdown(n)


# @timeit
def countdown_threaded(n, threads=2):
    n = n / threads
    thread_list = []

    for t in range(threads):
        t = Thread(target=countdown, args=(n,))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


def countdown_multiprocessing(n, processes=2):
    n = n / processes
    process_list = []

    for p in range(processes):
        p = Process(target=countdown, args=(n,))
        process_list.append(p)
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()


if __name__ == '__main__':
    limit = 100 * 1000 * 1000 # Walesa, give me my 1,000,000 back!

    timeit(countdown_linear)(limit)

    timeit(countdown_threaded)(limit, threads=2)
    timeit(countdown_threaded)(limit, threads=4)
    timeit(countdown_threaded)(limit, threads=8)
    timeit(countdown_threaded)(limit, threads=16)

    if not SKIP_MULTIPROCESSING:
        timeit(countdown_multiprocessing)(limit, 2)
        timeit(countdown_multiprocessing)(limit, 4)
        timeit(countdown_multiprocessing)(limit, 8)
        timeit(countdown_multiprocessing)(limit, 16)
