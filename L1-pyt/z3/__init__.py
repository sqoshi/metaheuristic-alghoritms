import itertools
import random
import signal
import copy
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
    t, n, m = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line if x != '\n'])
        line = f.readline()
    return t, int(n), int(m), array


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
    print(list)
    for i in range(0, len(list)):
        l = copy.deepcopy(list)
        for j in range(0, len(list)):
            z = swapPositions(l, i, j)
            if z not in result:
                result.append(z)
    return result


def findStartPosition(b):
    board = b.copy()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 5:
                return j, i


def getNeighbours(x, y, board):
    D = board[y + 1][x]
    U = board[y - 1][x]
    L = board[y][x - 1]
    R = board[y][x + 1]
    return [U, D, L, R]


def checkMove(x, y, board):
    if board[y][x] == 0:
        return 1
    elif board[y][x] == 1:
        return -1
    else:
        return 0


def move(x, y, direction, board):
    if direction == "UP":
        if checkMove(x, y - 1, board):
            board[y][x], board[y - 1][x] = board[y - 1][x], board[y][x]
    elif direction == "DOWN":
        if checkMove(x, y + 1, board):
            board[y][x], board[y + 1][x] = board[y + 1][x], board[y][x]
    elif direction == "LEFT":
        if checkMove(x - 1, y, board):
            board[y][x], board[y][x - 1] = board[y][x - 1], board[y][x]
    elif direction == "RIGHT":
        if checkMove(x + 1, y, board):
            board[y][x + 1], board[y][x] = board[y][x], board[y][x + 1]


def initialSolution(board, x, y):
    counter = 0
    path = []
    b = board.copy()
    # x, y = findStartPosition(list(b))
    currentX, currentY = x, y
    neighs = getNeighbours(x, y, b)
    while not neighs.__contains__(1):
        for x in b:
            print(x)
        print('\n')
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[0] != 1:
            move(currentX, currentY, "UP", b)
            counter += 1
            currentY -= 1
            path.append('U')
        print(counter)
    while neighs[0] == 1:
        for x in b:
            print(x)
        print('\n')
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[0] == 8:
            return path + ['U']
        if neighs[3] != 1:
            move(currentX, currentY, "RIGHT", b)
            currentX += 1
            path.append('R')
        if neighs[3] == 1:
            break
    while neighs[3] == 1:
        for x in b:
            print(x)
        print('\n')
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[3] == 8:
            return path + ['R']
        if neighs[1] != 1:
            move(currentX, currentY, "DOWN", b)
            currentY += 1
            path.append('D')
        if neighs[1] == 1:
            break
    while neighs[1] == 1:
        for x in b:
            print(x)
        print('\n')
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[1] == 8:
            return path + ['D']
        if neighs[2] != 1:
            move(currentX, currentY, "LEFT", b)
            currentX -= 1
            path.append('L')
        if neighs[2] == 1:
            break
    while neighs[2] == 1:
        for x in b:
            print(x)
        print('\n')
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[2] == 8:
            return path + ['L']
        if neighs[0] != 1:
            move(currentX, currentY, "UP", b)
            currentY -= 1
            path.append('U')
        if neighs[0] == 1:
            break
    # for x in b:
    # print(x)


global CurrentBestPath
global CurrentBestDist


def tabu_search(board):
    global CurrentBestPath
    global CurrentBestDist
    x0, y0 = findStartPosition(list(board))
    copy_list = copy.deepcopy(board)
    initial = initialSolution(copy_list, x0, y0)
    CurrentBestPath, CurrentBestDist = initial, len(initial)
    print(CurrentBestDist, CurrentBestPath)
    x = initial
    print(x)
    T = []
    for x in board:
        print(x)
    neighbours = findAllSwaps(x[:len(x) - 1])
    print(neighbours)


def main():
    t, n, m, b = readData("board")
    try:
        with time_limit(int(t)):
            tabu_search(b)
    except TimeoutException:
        print("Timed out!")


main()
