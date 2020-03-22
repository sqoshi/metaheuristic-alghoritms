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

def sumOfQuadrates(l):
    s = 0
    for x in l:
        s += pow(x, 2)
    return s


def productOfCos(l):
    p = 1
    for i in range(len(l)):
        p *= cos(l[i] / sqrt(i + 1))
    return p


def griewank(l):
    s = sumOfQuadrates(l)
    p = productOfCos(l)
    return 1 + s - p


def happyCat(l):
    x = numpy.linalg.norm(l)
    x2 = pow(x, 2)
    return 0.5 + pow(pow(x2 - 4, 2), 0.125) + 0.25 * (
            0.5 * x2 + sum(l))


def generateNeighbour(x):
    res = []
    for i in range(4):
        res.append(x[i] + e * (random.uniform(-0.05, 0.05)))
    return res


def chooseFunction(b):
    if b == 0:
        f = happyCat
    else:
        f = griewank
    return f


def main(S, b):
    fs = open("output", "w")
    f = chooseFunction(b)
    fs.write(str(f))
    fs.write("\n")
    while 1:
        neighbour = generateNeighbour(S)
        if f(S) > f(neighbour):
            S = neighbour
            m = "{0}{1}\n".format(str(S), str(f(S)))
            fs.write(m)


def findLocalMin(t, b):
    S = [1, 2, 3, 4]
    try:
        with time_limit(t):
            main(S, b)
    except TimeoutException as e:
        print("Timed out!")


findLocalMin(60, 1)
