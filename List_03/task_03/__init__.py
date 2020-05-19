import time

import matplotlib.pyplot as plt
import numpy as np


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
    t, n, m, s, p = line.split()
    line = f.readline()
    board = []
    paths = []
    i = 0
    while line:
        if i < int(n):
            board.append([int(x) for x in line if x != '\n'])
        else:
            paths.append(line if '\n' not in line else line[:len(line) - 2])
        line = f.readline()
        i += 1
    return int(t), int(n), int(m), int(s), int(p), paths, np.array(board)


def get_start(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 5:
                return int(j), int(i)


def get_millis(seconds):
    return seconds * 10 ** 3


def get_current_time():
    return get_millis(int(time.time()))


def get_min(paths_list):
    return min(paths_list, key=len)


def validate_indexes(i, j, path, limit):
    while i == j or path[i] == path[j]:
        j = np.random.randint(0, limit)


def get_random_indexes(path):
    limit = len(path)
    i = np.random.randint(0, limit)
    j = np.random.randint(0, limit)
    validate_indexes(i, j, path, limit)
    return i, j


def swap(path):
    path_list = list(path)
    i, j = get_random_indexes(path)
    path_list[j], path_list[i] = path_list[i], path_list[j]
    return ''.join(path_list)


def get_upper(x, y, board):
    return board[y - 1][x]


def get_lower(x, y, board):
    return board[y + 1][x]


def get_left(x, y, board):
    return board[y][x - 1]


def get_right(x, y, board):
    return board[y][x + 1]


def get_neighbours(x, y, board):
    return [get_left(x, y, board), get_upper(x, y, board), get_right(x, y, board), get_lower(x, y, board)]


def append_step(path, neighbours_list):
    index = neighbours_list.index(8)
    directions = ['L', 'U', 'R', 'D']
    return path + directions[index]


def detect_wall(x, y, path, board):
    endX, endY = x, y
    for d in path:
        if board[endY][endX] == 1:
            return False
        if d == 'U':
            endY -= 1
        elif d == 'D':
            endY += 1
        elif d == 'R':
            endX += 1
        else:
            endX -= 1
        if len(board) - 1 > endY and len(board[0]) - 1 > endX:
            neighbours = get_neighbours(endX, endY, board)
            if 8 in neighbours:
                return append_step(path, neighbours)


def replace(path, board):
    x, y = get_start(board)
    new_path = swap(path)
    if not detect_wall(x, y, new_path, board):
        new_path = swap(path)
    return new_path


def tournament_selection(P, board):
    t = len(P)
    best = replace(np.random.choice(P), board)
    for _ in (1, t):
        beside = replace(np.random.choice(P), board)
        if len(beside) < len(best):
            best = beside
    return best


def get_new_2p(path1, path2, l):
    v, w = list(path1), list(path2)
    c, d = np.random.randint(1, l), np.random.randint(1, l)
    if c > d:
        c, d = d, c
    if c != d:
        for i in range(c, d):
            v[i], w[i] = w[i], v[i]
    return ''.join(v), ''.join(w)


def two_point_crossover(path1, path2, board):
    x, y = get_start(board)
    l = min(len(path1), len(path2))
    new_path1, new_path2 = get_new_2p(path1, path2, l)
    while detect_wall(x, y, new_path1, board) and detect_wall(x, y, new_path2, board):
        new_path1, new_path2 = get_new_2p(path1, path2, l)
    return new_path1, new_path2


def genetic_algorithm(t, n, m, s, p, paths, board):
    end_time = get_millis(t) + get_current_time()
    P = paths
    # TODO: if s < P add random solution x p-s
    best = get_min(P)
    while get_current_time() < end_time:
        best = get_min(P)
        Q = []
        for _ in range(int(s / 2)):
            Pa = tournament_selection(P, board)
            Pb = tournament_selection(P, board)
            Ca, Cb = two_point_crossover(Pa.copy(), Pb.copy(), board)
            print(Pa, Pb)
    return best


def main():
    t, n, m, s, p, paths, board = read_data('tests/t2')
    print(t, n, m, s, p)
    print(paths)
    for level in board:
        print(level)
    genetic_algorithm(t, n, m, s, p, paths, board)


main()
