import itertools
import random
import signal
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
    initial = initialSolution(graph, n, src)
    calculateDistance(graph, initial)
    CurrentBestPath, CurrentBestDist = initial, calculateDistance(graph, initial)
    x = initial
    T = []
    bestSols = []
    cycles = 1
    # neighbours = makeCycles(findAllSwaps(x[1:len(x) - 1]), src)
    while cycles < 150:
        cycles += 1
        neighbours = makeCycles(findAllSwaps(x[1:len(x) - 1]), src)
        mins = calculateDistance(graph, neighbours[0])
        for neigh in neighbours:
            if neigh not in T:
                sample = calculateDistance(graph, neigh)
                # print(sample, mins)
                if sample <= mins:
                    # print(neigh, sample, 'new')
                    mins = sample
                    x = neigh
                    if CurrentBestDist >= sample:
                        print('- Actual Minimal Distance-', sample, neigh)
                        CurrentBestDist = sample
                        CurrentBestPath = x
                        BestSolutions.append((x, sample))
                    T.append(neigh)
            CurrentBestPath = x
        # print('Best', CurrentBestDist, CurrentBestPath)
    tabu_search(graph, n, random.randint(0, n))  # resetuje wyszukiwanie w innym wierzcholku jesli wpadl w lokalne min


BestSolutions = []


def main():
    t, n, g = readData("data1")
    try:
        with time_limit(int(t)):
            tabu_search(g, int(n), 5)
    except TimeoutException:
        print("Timed out!")
        print(CurrentBestPath)
        print(CurrentBestDist)
        print(min(BestSolutions, key=lambda t: t[1]))


main()
