import random
import copy
import sys
import time
import tkinter as tk
import numpy as np
import numpy.random as rn
import matplotlib.pyplot as plt


def plot_graph(costs):
    """Graphs plot for costs"""
    plt.figure()
    plt.plot(costs, 'b')
    plt.title("Costs")
    plt.show()


def read_data(filename):
    """Reads data from file"""
    f = open(filename, "r")
    line = f.readline()
    t, n, m = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line if x != '\n'])
        line = f.readline()
    return int(t), int(n), int(m), array


def swap_elements(list, pos1, pos2):
    """Function that swaps elements of list and return it, not changing primal list"""
    l = list.copy()
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l


def find_initial_position(b):
    """Function finds initial position of traveller"""
    board = b.copy()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 5:
                return int(j), int(i)


def get_neighbours(x, y, board):
    """Return neighbours of place"""
    D = board[y + 1][x]
    U = board[y - 1][x]
    L = board[y][x - 1]
    R = board[y][x + 1]
    return [U, D, L, R]


def check_move(new_x, new_y, board):
    """Validates move"""
    if board[new_y][new_x] == 0:
        return 0
    elif board[new_y][new_x] == 1:
        return -1
    else:
        return 1


def move(board, x, y, direct):
    """Moves traveller by one up,right,down or left"""
    new_x, new_y = x, y
    if direct == 'U':
        if check_move(x, y - 1, board) == 0:
            new_y = y - 1
            board[y][x], board[y - 1][x] = board[y - 1][x], board[y][x]
        elif check_move(x, y - 1, board) == -1:
            pass
    elif direct == 'D':
        if check_move(x, y + 1, board) == 0:
            new_y = y + 1
            board[y][x], board[y + 1][x] = board[y + 1][x], board[y][x]
        elif check_move(x, y + 1, board) == -1:
            pass
    elif direct == 'L':
        if check_move(x - 1, y, board) == 0:
            new_x = x - 1
            board[y][x], board[y][x - 1] = board[y][x - 1], board[y][x]
        elif check_move(x - 1, y, board) == -1:
            pass
    else:
        if check_move(x + 1, y, board) == 0:
            new_x = x + 1
            board[y][x], board[y][x + 1] = board[y][x + 1], board[y][x]
        elif check_move(x + 1, y, board) == -1:
            pass
    return board, new_x, new_y


def printM(M):
    """Display map"""
    print()
    print('\n'.join([''.join(['{:0}'.format(item) for item in row])
                     for row in M]))
    print()


def explore(board, x0, y0, path):
    """In this function agent is exploring the map - goes randomly everywhere one by one till meets wall.
    After meeting wall he stays and returns his path."""
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


def random_path(n, m):
    """Gets random path: size 2*(n+m-1), without repetitions"""
    dirs = ['U', 'D', 'L', 'R']
    size = n * m - 2 * (n + m - 1)
    rand_path = [random.choice(dirs) for x in range(size)]
    rand_path = remove_constant_points(rand_path)
    while len(rand_path) != size:
        part = [random.choice(dirs) for x in range(size - len(rand_path))]
        rand_path.extend(part)
        rand_path = remove_constant_points(rand_path)
    return rand_path


def get_neighbour(list):
    """Returns transpositin of proper path"""
    i = random.randint(0, len(list) - 1)
    j = random.randint(0, len(list) - 1)
    while i == j:
        j = random.randint(0, len(list) - 1)
    return swap_elements(list, i, j)


def check_way(board, x, y, path):
    """Checks if after path traveller is in exit and during the way he has not met a wall."""
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


def initial_solution(b, x, y):
    """Finds initial solution for simulated annealing (random,stay,radnom,stay ...)
    Traveller follows random path till he meets wall, than he stays and loss other path.
    Procedure is being followed until he finds exit."""
    board = copy.deepcopy(b)
    full_path = []
    n = len(board)
    m = len(board[0])
    b = copy.deepcopy(board)
    startX, startY = x, y

    while 8 not in get_neighbours(x, y, b):
        sec, x, y, b = explore(b, x, y, random_path(n, m))
        full_path.extend(sec)
    full_path.append(choose_dir(get_neighbours(x, y, b).index(8)))
    full_path = remove_constant_points(full_path)
    check_way(board, startX, startY, full_path)

    return full_path


def choose_dir(z):
    """Choosing direction by given number"""
    if z == 0:
        return 'U'
    elif z == 1:
        return 'D'
    elif z == 2:
        return 'L'
    elif z == 3:
        return 'R'


def remove_constant_points(li):
    """ IF we have situation that traveller went up and back like UP or RL we can clean it from path."""
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


def simulated_annealing(t, b, T0, graph):
    """Simulated annealing"""
    # Find end time
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    # Get initial position
    x0, y0 = find_initial_position(b)
    # Find initial solution
    state = initial_solution(b, x0, y0)
    cost = len(state)
    # initialize our history
    states, costs = [state], [cost]
    step = 1
    # While time is up and temp is bigger than 0
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        # decrease temperature
        T = T * 0.9995
        # get neighbour
        new_state = remove_constant_points(get_neighbour(state))
        # while way is not proper, get other neighbour
        while not check_way(b, x0, y0, new_state):
            new_state = remove_constant_points(get_neighbour(state))
        # get cost of gooooood neighbour
        new_cost = len(new_state)
        # check probability
        if acceptance_probability(cost, new_cost, T) > rn.random():
            # move to neighbour
            state, cost = new_state, new_cost
            # check bests
            if costs[len(costs) - 1] > cost:
                states.append(state)
                costs.append(cost)
    # plot costs
    if graph:
        plot_graph(costs)
    return costs[len(costs) - 1], states[len(states) - 1]


def main():
    # t, n, m, b = readData('tests/t2')
    t, n, m = [int(x) for x in input().split()]
    arr = []
    for i in range(n):
        z = list(input())
        arr.append([int(x) for x in z if x != '\n'])
    b = arr
    c, s = simulated_annealing(t, b, T0=100, graph=False)
    z = ''.join(s)
    print(c)
    sys.stderr.write(z)


main()


def visualise(n, m, b):
    """Visualise"""
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
