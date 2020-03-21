import signal
from math import sqrt, cos
import random
import signal
from contextlib import contextmanager

e = 0.01


class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


# algorytm zaczyna sie pnizej

def sumOfQuadrates(a, b, c, d):
    l = [a, b, c, d]
    s = 0
    for x in l:
        s += pow(x, 2)
    return s


def productOfCos(a, b, c, d):
    l = [a, b, c, d]
    p = 1
    for i in range(len(l)):
        p *= cos(l[i] / sqrt(i + 1))
    return p


def griewank(l, i):
    s = sumOfQuadrates(l[i], l[i + 1], l[i + 2], l[i + 3])
    p = productOfCos(l[i], l[i + 1], l[i + 2], l[i + 3])
    return 1 + s - p


def generateNeigh(x):
    l = [x]
    for i in range(1000):
        l.append(l[len(l) - 1] + e * (random.uniform(-0.05, 0.05)))
    return l


def program(S):
    while 1:
        neighs = generateNeigh(S)
        for i in range(len(neighs) - 4):
            if griewank(neighs, i) > griewank(neighs, i + 1):
                S = neighs[i + 1]
                index = i + 1
        print(neighs[:4], griewank(neighs, index))


try:
    with time_limit(120):
        program(1.4)
except TimeoutException as e:
    print("Timed out!")
