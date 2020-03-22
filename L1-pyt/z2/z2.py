import signal
from contextlib import contextmanager
import numpy as np


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

def readData():
    f = open("data", "r")
    line = f.readline()
    t, n = line.split()
    array = []
    while line:
        array.append(line.split())
        line = f.readline()
    array.remove(array[0])
    return t, n, array


def program(graph):
    print(np.matrix(graph))


def init():
    t, n, graph = readData()
    try:
        with time_limit(int(t)):
            program(graph)
    except TimeoutException as e:
        print("Timed out!")


init()
