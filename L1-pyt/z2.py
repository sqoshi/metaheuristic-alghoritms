import random
import signal
import tsp
from contextlib import contextmanager
from collections import defaultdict
import numpy as np, pandas as pd
import itertools

global result


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
    f = open("z2/data1", "r")
    line = f.readline()
    t, n = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line.split()])
        line = f.readline()
    return t, n, array


# tu mam blad to trzeba ogarnac
def findMinimalDistance(lis, T):
    l = lis.copy()
    tabuElsIncurrentRow = [lis[t] for t in T]
    print(l, tabuElsIncurrentRow)
    diff = list(set(l).difference(tabuElsIncurrentRow))
    if len(diff) == 0:
        print(T)
        raise Exception
    else:
        minDistance = min(diff)
    index = lis.index(minDistance)
    print(index, 'inde')
    return minDistance, index


def calculateDistance(graph, path):
    distance = 0
    for i in range(0, len(path) - 1):
        distance += graph[path[i]][path[i + 1]]
    return distance


def swapPositions(list, pos1, pos2):
    l = list.copy()
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l


def findFirstSolution(graph, n):
    start = 0  # random.randint(0, n - 1)
    totalDistance = 0
    x = start
    # print('Wylosowalem start:', start)
    T = [start]
    while len(T) < n:
        neighbours = graph[x]
        try:
            minDistance, cityIndex = findMinimalDistance(neighbours, T)
        except:
            print('es')
            break
        x = cityIndex
        totalDistance += minDistance
        print('Przechodze do kolejnego miasta:', x, 'aktualny koszt:', totalDistance, T)
        T.append(x)
    totalDistance += graph[T[len(T) - 1]][start]
    T.append(start)
    return T, totalDistance


def findAllSwaps(list):
    result = []
    for i, j in itertools.combinations([i for i in range(len(list))], 2):
        result.append(swapPositions(list, i, j))
    return result


def tabu_search(graph, n):
    global result
    bestSolutions = []
    print(graph)
    path, dist = findFirstSolution(graph, int(n))
    path = [x for x in range(int(n))] + [0]
    dist = calculateDistance(graph, path)
    print(path, dist)
    T = []
    x = path
    bestSolutions.append((x, dist))
    startOfCycle = path[0]
    while True:
        result = min(bestSolutions, key=lambda t: t[1])
        distances = []
        l1 = findAllSwaps(x[1:len(x) - 1])
        print(l1)
        neighbours = [m for m in l1 if m not in T]
        for neighbour in neighbours:
            neighbour.insert(0, startOfCycle)
            neighbour.append(startOfCycle)
            distances.append(calculateDistance(graph, neighbour))
        minDist = min(distances)
        print(distances)
        index = distances.index(minDist)
        minPath = neighbours[index]
        pair = (minPath, minDist)
        if pair not in T:
            bestSolutions.append(pair)
        T.extend([m for m in neighbours if m not in T])
        # if calculateDistance(graph, minPath) <= calculateDistance(graph, x):
        x = minPath


def main():
    t, n, g = readData()
    try:
        with time_limit(int(t)):
            tabu_search(g, n)
    except TimeoutException:
        print("Timed out!\n", result)


main()
