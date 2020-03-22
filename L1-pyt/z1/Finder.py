import operator
from math import sqrt, cos
import random
import signal
import sys
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


""" 
Wartosci zostaly wyznaczone eksperymentalnie!
"""


def chooseFunction(b):
    if b == 0:
        f = happyCat
        l = 1.0e-6
    else:
        f = griewank
        l = 1.0e-9

    return f, l


def findMin(b, out):
    size = random.randint(0, 200)
    S = [random.uniform(-size, size), random.uniform(-size, size)
        , random.uniform(-size, size), random.uniform(-size, size)]
    f = open(out, "w")
    mins = []
    function, limit = chooseFunction(b)
    while 1:
        neighbour = generateNeighbour(S)
        fs = function(S)
        fn = function(neighbour)
        diff = fs - fn
        if diff > 0:
            # ucieczka z lokalnego min i spawn w nowym losowym miejscu. @@@@RESET@@@
            if diff < limit:  # ta magiczna liczba zostala wyznaczona eksperymentalnie na podstawie prob
                mins.append((S, fs))
                S = [random.uniform(-size, size), random.uniform(-size, size)
                    , random.uniform(-size, size), random.uniform(-size, size)]
                m = "{0}\n".format(min(mins, key=operator.itemgetter(1)))
                f.seek(0)
                f.write(m)
            else:
                S = neighbour


def main(t, b, out):
    try:
        with time_limit(t):
            findMin(b, out)
    except TimeoutException:
        print("Timed out!")


main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
