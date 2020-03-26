import random
import signal
import tsp
from contextlib import contextmanager
from collections import defaultdict
import numpy as np, pandas as pd


class TimeoutException(Exception):
    pass


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


def readData():
    f = open("data", "r")
    line = f.readline()
    t, n = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line.split()])
        line = f.readline()
    return t, n, array


def initial(graphAdj, n, s):
    start = s
    notVisited = [int(x) for x in range(n)]
    notVisited.remove(s)
    path = [s]
    while graphAdj[path[len(path) - 1]][start] == 0:
        while len(notVisited) > 0:
            nextCity = random.choice(notVisited)
            # jesli odleglosc do danego miasta jest zerem musimy wylosowac inne miasto.
            while graphAdj[s][nextCity] == 0:
                nextCity = random.choice(notVisited)
            # wchodzimy do miasta nowego i usuwamy go z listy
            if graphAdj[s][nextCity] != 0:
                notVisited.remove(nextCity)
            s = nextCity
            path.append(s)
    return path + [start]


def findMinimalDistance(lis, T):
    l = lis.copy()
    tabuElsIncurrentRow = [lis[t] for t in T]
    diff = list(set(l).difference(tabuElsIncurrentRow))
    if len(diff) == 0:
        raise Exception
    else:
        minDistance = min(diff)
    # print(l, T, 'Wybieram z :', diff)
    index = lis.index(minDistance)
    # print('minimalnyDistance, index = ', minDistance, ',', index)
    return minDistance, index


def findFirstSolution(graphAdj, n):
    start = random.randint(0, n - 1)
    totalDistance = 0
    x = start
    # print('Wylosowalem start:', start)
    T = [start]
    while len(T) < n:
        neighbours = graphAdj[x]
        try:
            minDistance, cityIndex = findMinimalDistance(neighbours, T)
        except:
            break
        x = cityIndex
        totalDistance += minDistance
        # print('Przechodze do kolejnego miasta:', x, 'aktualny koszt:', totalDistance, T)
        T.append(x)
    totalDistance += graphAdj[T[len(T) - 1]][start]
    print(graphAdj[T[len(T) - 1]][start])
    T.append(start)
    return T, totalDistance


def tabu_search(graphAdj, n):
    print(graphAdj)
    path, dist = findFirstSolution(graphAdj, int(n))
    print(path, dist)


def main():
    t, n, g = readData()
    try:
        with time_limit(int(t)):
            tabu_search(g, n)
    except TimeoutException:
        print("Timed out!")


main()
