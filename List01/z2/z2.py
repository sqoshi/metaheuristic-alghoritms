import itertools
import random
import signal
import sys
from contextlib import contextmanager


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


def readData(filename):
    f = open(filename, "r")
    line = f.readline()
    t, n = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line.split()])
        line = f.readline()
    return t, n, array


def calculateDistance(graph, path):
    distance = 0
    for i in range(0, len(path) - 1):
        distance += graph[path[i]][path[i + 1]]
    return distance


def swapPositions(list, pos1, pos2):
    l = list.copy()
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l


def findAllSwaps(list):
    result = []
    for i, j in itertools.combinations([i for i in range(len(list))], 2):
        result.append(swapPositions(list, i, j))
    return result


def findNextCity(graph, T):
    city = T[0]
    initialMinium = 0
    row = graph[T[len(T) - 1]]
    for i in range(len(row)):
        if i not in T:
            if initialMinium > row[i] or initialMinium == 0:
                initialMinium = row[i]
                city = i
    return city


def initialSolution(graph, n, src):
    T = [src]
    for i in range(n):
        minimalCity = findNextCity(graph, T)
        T.append(minimalCity)
    return T


def makeCycles(list, src):
    for element in list:
        element.insert(0, src)
        element.append(src)
    return list


global CurrentBestPath
global CurrentBestDist


def tabu_search(graph, n, src):
    global CurrentBestPath
    global CurrentBestDist
    global BestSolutions
    limit = 100
    if n < 25:
        limit = 10000
    initial = initialSolution(graph, n, src)
    calculateDistance(graph, initial)
    CurrentBestPath, CurrentBestDist = initial, calculateDistance(graph, initial)
    x = initial
    T = []
    cycles = 1
    # best is 26 vertex!
    while cycles < limit:
        cycles += 1
        neighbours = makeCycles(findAllSwaps(x[1:len(x) - 1]), src)
        mins = calculateDistance(graph, neighbours[0])
        for neigh in neighbours:
            if neigh not in T:
                sample = calculateDistance(graph, neigh)
                if sample <= mins:
                    mins = sample
                    x = neigh
                    if CurrentBestDist >= sample:
                        CurrentBestDist = sample
                        CurrentBestPath = x
                        BestSolutions.append((x, sample))
                    T.append(neigh)
            CurrentBestPath = x
    tabu_search(graph, n,
                random.randint(0, n - 1))  # resetuje wyszukiwanie w innym wierzcholku jesli wpadl w lokalne min


BestSolutions = []


def main():
    t, n = [int(x) for x in input().split()]
    g = [[int(x) for x in input().split()] for i in range(n)]
    # t, n, g = readData(sys.argv[1])
    src = 0
    # bo wybieram 26 miasto jako pierwssze :D
    if int(n) > 27:
        src = 26
    try:
        with time_limit(int(t)):
            tabu_search(g, int(n), src)
    except TimeoutException:
        print(min(BestSolutions, key=lambda t: t[1]))


main()
