"""

Measures on 4 core Intel cpu:

+-------------+--------+-------+-------+-------+-------+
|             | linear | 2x    | 4x    | 8x    | 16x   |
+-------------+--------+-------+-------+-------+-------+
| Python 2.6  | 6,5    | 5,4   | 3,3   | 1,7   | 1,0   |
+-------------+--------+-------+-------+-------+-------+
| Python 2.7  | 7,1    | 5,7   | 3,3   | 1,6   | 0,9   |
+-------------+--------+-------+-------+-------+-------+
| Python 3.2  | 9,6    | 15,5  | 7,5   | 3,9   | 1,8   |
+-------------+--------+-------+-------+-------+-------+
| Python 3.3  | 9,7    | 15,2  | 7,3   | 3,7   | 1,8   |
+-------------+--------+-------+-------+-------+-------+
| Pypy        | 0,1    | 0,2   | 0,1   | 0,1   | < 0,1 |
+-------------+--------+-------+-------+-------+-------+
| Jython      | 4,0    | 1,0   | 0,4   | 0,2   | 0,1   |
+-------------+--------+-------+-------+-------+-------+
| IronPython  | not measured                           |
+-------------+--------+-------+-------+-------+-------+


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
| Pypy        | 0,1    | 0,3   | 0,1   | 0,1   | < 0,1 |
+-------------+--------+-------+-------+-------+-------+
| Jython      | 4,6    | 1,4   | 1,0   | 0,1   | 0,1   |
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


# @timeit
def countdown_linear(n):
    countdown(n)


# @timeit
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
    timeit(countdown_linear)(limit)
    timeit(countdown_threaded)(limit, threads=2)
    timeit(countdown_threaded)(limit, threads=4)
    timeit(countdown_threaded)(limit, threads=8)
    timeit(countdown_threaded)(limit, threads=16)
