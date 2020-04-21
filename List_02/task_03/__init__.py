import random
import copy
import time
import tkinter as tk
import numpy as np
import numpy.random as rn
import matplotlib.pyplot as plt


def plot_graphs(costs):
    plt.figure()
    plt.plot(costs, 'b')
    plt.title("Costs")
    plt.show()


def readData(filename):
    f = open(filename, "r")
    line = f.readline()
    t, n, m = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line if x != '\n'])
        line = f.readline()
    return int(t), int(n), int(m), array


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
    for i in range(0, len(list)):
        l = copy.deepcopy(list)
        for j in range(0, len(list)):
            z = swapPositions(l, i, j)
            el = ' '.join([str(elem) for elem in z])
            if z not in result:
                result.append(z)
    return result


def findStartPosition(b):
    board = b.copy()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 5:
                return int(j), int(i)


def getNeighbours(x, y, board):
    D = board[y + 1][x]
    U = board[y - 1][x]
    L = board[y][x - 1]
    R = board[y][x + 1]
    return [U, D, L, R]


def checkMove(new_x, new_y, board):
    if board[new_y][new_x] == 0:
        return 0
    elif board[new_y][new_x] == 1:
        return -1
    else:
        return 1


def move(board, x, y, direct):
    new_x, new_y = x, y
    if direct == 'U':
        if checkMove(x, y - 1, board) == 0:
            new_y = y - 1
            board[y][x], board[y - 1][x] = board[y - 1][x], board[y][x]
        elif checkMove(x, y - 1, board) == -1:
            pass
    elif direct == 'D':
        if checkMove(x, y + 1, board) == 0:
            new_y = y + 1
            board[y][x], board[y + 1][x] = board[y + 1][x], board[y][x]
        elif checkMove(x, y + 1, board) == -1:
            pass
    elif direct == 'L':
        if checkMove(x - 1, y, board) == 0:
            new_x = x - 1
            board[y][x], board[y][x - 1] = board[y][x - 1], board[y][x]
        elif checkMove(x - 1, y, board) == -1:
            pass
    else:
        if checkMove(x + 1, y, board) == 0:
            new_x = x + 1
            board[y][x], board[y][x + 1] = board[y][x + 1], board[y][x]
        elif checkMove(x + 1, y, board) == -1:
            pass
    return board, new_x, new_y


def printM(M):
    print()
    print('\n'.join([''.join(['{:0}'.format(item) for item in row])
                     for row in M]))
    print()


def explore(board, x0, y0, path):
    b = copy.deepcopy(board)
    x, y = x0, y0
    i = 0
    index = i
    while i >= 0:
        history = copy.deepcopy(b)
        b, x, y = move(b, x, y, path[i])
        if history == b:
            index = i
            i = -999
            break
        i += 1
    return path[:index], x, y, b


def randomPath(n, m):
    dirs = ['U', 'D', 'L', 'R']
    size = n * m - 2 * (n + m - 1)
    rand_path = [random.choice(dirs) for x in range(size)]
    rand_path = removeConsts(rand_path)
    while len(rand_path) != size:
        part = [random.choice(dirs) for x in range(size - len(rand_path))]
        rand_path.extend(part)
        rand_path = removeConsts(rand_path)
    return rand_path


def getNeighbour(list):
    i = random.randint(0, len(list) - 1)
    j = random.randint(0, len(list) - 1)
    while i == j:
        j = random.randint(0, len(list) - 1)
    return swapPositions(list, i, j)


def isInGate(board, x, y, path):
    endX, endY = x, y
    for d in path:
        if d == 'U':
            endY -= 1
        elif d == 'D':
            endY += 1
        elif d == 'R':
            endX += 1
        else:
            endX -= 1
        if board[endY][endX] == 1:
            return False
        elif board[endY][endX] == 8:
            return True


def initialSolution(b, x, y):
    board = copy.deepcopy(b)
    full_path = []
    n = len(board)
    m = len(board[0])
    b = copy.deepcopy(board)
    startX, startY = x, y
    while 8 not in getNeighbours(x, y, b):
        sec, x, y, b = explore(b, x, y, randomPath(n, m))
        full_path.extend(sec)
    full_path.append(chooseDir(getNeighbours(x, y, b).index(8)))
    full_path = removeConsts(full_path)
    isInGate(board, startX, startY, full_path)
    return full_path


def chooseDir(z):
    if z == 0:
        return 'U'
    elif z == 1:
        return 'D'
    elif z == 2:
        return 'L'
    elif z == 3:
        return 'R'


def removeConsts(li):
    z = ''.join(li)
    while "UD" in z or "DU" in z or "LR" in z or "RL" in z:
        z = z.replace("UD", "")
        z = z.replace("DU", "")
        z = z.replace("LR", "")
        z = z.replace("RL", "")
    return list(z)


def acceptance_probability(cost, new_cost, temp):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temp)
        return p


def simulated_annealing(t, b, T0):
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    x0, y0 = findStartPosition(b)
    state = initialSolution(b, x0, y0)
    cost = len(state)
    states, costs = [state], [cost]
    step = 1
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        T = T * 0.9995
        new_state = removeConsts(getNeighbour(state))
        while not isInGate(b, x0, y0, new_state):
            new_state = removeConsts(getNeighbour(state))
        new_cost = len(new_state)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            if costs[len(costs) - 1] > cost:
                states.append(state)
                costs.append(cost)
    plot_graphs(costs)
    return costs[len(costs) - 1], states[len(states) - 1], states, costs


def main():
    t, n, m, b = readData('tests/t2')
    print(simulated_annealing(t, b, 100))


main()


def visualise(n, m, b):
    window = tk.Tk()

    for i in range(n):
        for j in range(m):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j)
            label = tk.Label(master=frame, text=f"{b[i][j]}")
            label.pack()

    window.mainloop()
