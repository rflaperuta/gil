"""

Measures on 8 core AMD cpu:

+-------------+--------+-------+-------+-------+-------+
|             | linear | 2x    | 4x    | 8x    | 16x   |
+-------------+--------+-------+-------+-------+-------+
| Python 2.6  | 6,8    | 9,6   | 6,3   | 3,0   | 1,5   |
+-------------+--------+-------+-------+-------+-------+
| Python 2.7  | 7,4    | 10,0  | 6,5   | 3,3   | 1,6   |
+-------------+--------+-------+-------+-------+-------+
| Python 3.2  | 8,3    | 14,9  | 6,4   | 3,0   | 1,5   |
+-------------+--------+-------+-------+-------+-------+
| Python 3.3  | 8,0    | 14,9  | 6,5   | 3,3   | 1,5   |
+-------------+--------+-------+-------+-------+-------+
| Pypy        | 0,2    | 0,3   | 0,1   | 0,1   | < 0,1 |
+-------------+--------+-------+-------+-------+-------+
| Jython      | not measured                           |
+-------------+--------+-------+-------+-------+-------+
| IronPython  | not measured                           |
+-------------+--------+-------+-------+-------+-------+

"""

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


@timeit
def countdown_linear(n):
    countdown(n)


@timeit
def countdown_threaded(n, threads=2):
    n = n / threads
    thread_list = []

    for t in range(threads):
        t = Thread(target=countdown, args=(n / threads,))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


if __name__ == '__main__':
    limit = 100 * 1000 * 1000 # Walesa, give me my 1,000,000 back!
    countdown_linear(limit)
    countdown_threaded(limit, threads=2)
    countdown_threaded(limit, threads=4)
    countdown_threaded(limit, threads=8)
    countdown_threaded(limit, threads=16)
