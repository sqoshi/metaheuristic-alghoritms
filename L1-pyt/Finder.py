import signal
from math import sqrt, cos
import random
import signal
from contextlib import contextmanager

import numpy

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


def happyCat(l, i):
    p1 = numpy.linalg.norm(l[i:i + 3])
    return 1 / 2 + pow(pow(pow(p1, 2) - 4, 2), 1 / 8) + \
           1 / 4 * (1 / 2 * pow(p1, 2) + sum(l[i:i + 3]))


def generateNeigh(x):
    l = [x]
    for i in range(1000):
        l.append(l[len(l) - 1] + e * (random.uniform(-0.05, 0.05)))
    return l


def chooseFunction(b):
    if b == 0:
        f = griewank
    else:
        f = happyCat
    return f


def program(S, b):
    f = chooseFunction(b)
    while 1:
        neighs = generateNeigh(S)
        for i in range(len(neighs) - 4):
            if f(neighs, i) > f(neighs, i + 1):
                S = neighs[i + 1]
                index = i + 1
        print(neighs[:4], griewank(neighs, index))


def findLocalMin(t, b):
    S = random.randint(-10, 10)
    try:
        with time_limit(t):
            program(S, b)
    except TimeoutException as e:
        print("Timed out!")


findLocalMin(60, 0)
