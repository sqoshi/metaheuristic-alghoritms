import time

import matplotlib.pyplot as plt
import numpy as np


def plot_graph(costs):
    """Graphs plot for costs"""
    plt.figure()
    print(np.array(costs).T)
    for i in range(len(np.array(costs).T)):
        plt.plot(np.array(costs)[:, i])
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


def mutate_transposition(path, board):
    path_transposed = swap(path)
    x, y = get_start(board)
    while not is_path_correct(x, y, path_transposed, board):
        path_transposed = swap(path)
    return remove_constant_points(path_transposed)


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


def is_path_correct(x, y, path, board):
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
    while not is_path_correct(x, y, new_path, board):
        new_path = swap(path)
    return new_path


def tournament_selection(P, board):
    t = len(P)
    best = replace(np.random.choice(P), board)
    for _ in (1, t):
        beside = replace(np.random.choice(P), board)
        if len(beside) < len(best):
            best = beside
    return best, beside


def slides_selection(P):
    total_len = sum([len(pi) for pi in P])
    quality = [len(pi) / total_len for pi in P]
    result = [False for _ in range(len(P))]
    while result.count(True) < 2:
        for i in range(len(result)):
            if result.count(True) == 2:
                break
            if np.random.uniform(0, 1) < quality[i]:
                result[i] = True
    return P[result.index(True)], P[result.index(True, 1)]


def selection(P):
    total_len = sum([len(pi) for pi in P])
    quality = [len(pi) / total_len for pi in P]
    max1 = min(quality)
    max1_ind = quality.index(max1)
    quality.remove(max1)
    max2 = min(quality)
    max2_ind = quality.index(max2)
    return P[max1_ind], P[max2_ind]


def remove_constant_points(path):
    z = path
    while "UD" in z or "DU" in z or "LR" in z or "RL" in z:
        z = z.replace("UD", "")
        z = z.replace("DU", "")
        z = z.replace("LR", "")
        z = z.replace("RL", "")
    return z


def cross_paths(path1, path2):
    l1, l2 = len(path1), len(path2)
    c1, d1 = np.random.randint(0, l1 - 1), np.random.randint(0, l1 - 1)
    c2, d2 = np.random.randint(0, l2 - 1), np.random.randint(0, l2 - 1)
    if c1 > d1:
        c1, d1 = d1, c1
    if c2 > d2:
        c2, d2 = d2, c2
    return path1[:c1] + path2[c2:d2] + path1[d1:], path2[:c2] + path1[c1:d1] + path1[d2:]


def two_point_crossover(path1, path2, board, n, m):
    x, y = get_start(board)
    new_path1, new_path2 = cross_paths(path1, path2)
    while not is_path_correct(x, y, remove_constant_points(new_path1), board) or \
            not is_path_correct(x, y, remove_constant_points(new_path2), board):
        new_path1, new_path2 = cross_paths(path1, path2)
    if len(path1) < n * m * len(new_path1):
        new_path1 = path1
    if len(path2) < n * m * len(new_path2):
        new_path2 = path2
    return remove_constant_points(new_path1), remove_constant_points(new_path2)


def genetic_algorithm(t, n, m, s, p, paths, board, graphs=True):
    end_time = get_millis(t) + get_current_time()
    P = paths
    # TODO: if s < P add random solution x p-s
    global_best = get_min(P)
    population_history = [[len(pi) for pi in P]]
    while get_current_time() <= end_time:
        # print(P)
        best = get_min(P)
        Q = []
        for _ in range(int(s / 2)):
            Pa, Pb = slides_selection(P)
            Ca, Cb = two_point_crossover(Pa, Pb, board, n, m)
            Q.append(mutate_transposition(Ca, board))
            Q.append(mutate_transposition(Cb, board))
            if len(best) < len(global_best):
                global_best = best
        P = Q
        population_history.append([len(pi) for pi in P])
        if graphs:
            plot_graph(population_history)
    return global_best, len(global_best)


def main():
    t, n, m, s, p, paths, board = read_data('tests/t2')
    print(t, n, m, s, p)
    print(paths)
    for level in board:
        print(level)
    result = genetic_algorithm(t, n, m, s, p, paths, board)
    print(result)


main()
