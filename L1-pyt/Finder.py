import operator
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


def main(b):
    S = [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)]
    f = open("output", "w")
    mins = []
    function = chooseFunction(b)
    f.write(str(f))
    f.write("\n")
    while 1:
        neighbour = generateNeighbour(S)
        fs = function(S)
        fn = function(neighbour)
        diff = fs - fn
        if diff > 0:
            # ucieczka z lokalnego min i spawn w nowym losowym miejscu.
            if diff < 1.5e-10:  # ta magiczna liczba zostala wyznaczona eksperymentalnie na podstawie prob
                print('Stucked in local min - new spawn.')
                mins.append((S, fs))
                S = [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)]
                print(min(mins, key=operator.itemgetter(1)))
            else:
                S = neighbour

        # m = "{0}{1}\n".format(str(S), str(f(S)))
        # f.write(m)


def findLocalMin(t, b):
    try:
        with time_limit(t):
            main(b)
    except TimeoutException:
        print("Timed out!")


def macheps():
    m = 1.0
    while not m / 2 == 0:
        m = m / 2
    print(m)


# macheps()
findLocalMin(60, 1)
