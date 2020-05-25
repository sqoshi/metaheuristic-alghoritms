import random
import time

import matplotlib.pyplot as plt
import numpy as np


# from task_03.Initial import initial_solution


def follow_way_succed(board, x, y, path):
    """
    Follow path and return path to entertance if found.
    :param board:
    :param x:
    :param y:
    :param path:
    :return:
    """
    step = 0
    endX, endY = x, y
    for d in path:
        step += 1
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
            return path[:step]


def random_path_by_size(size):
    """
    Function returns random path with size length.
    :param size:
    :return:
    """
    dirs = ['U', 'D', 'L', 'R']
    rand_path = [random.choice(dirs) for x in range(size)]
    rand_path = remove_constant_points(rand_path)
    while len(rand_path) != size:
        part = [random.choice(dirs) for x in range(size - len(rand_path))]
        rand_path.extend(part)
        rand_path = remove_constant_points(rand_path)
    return rand_path


def get_path_same_prefix(state, b):
    """
    Function takes a path and returns other path but with random length same suffix.
    :param state:
    :param b:
    :return:
    """
    state = list(state)
    x0, y0 = get_start(b)
    i = random.randint(0, len(state) - 1)
    part_state = state[:i]
    rest = random_path_by_size(len(state))
    part_state.extend(rest)
    new_state = part_state
    while not follow_way_succed(b, x0, y0, new_state):
        i = random.randint(0, len(state) - 1)
        part_state = state[:i]
        rest = random_path_by_size(len(state))
        part_state.extend(rest)
        new_state = part_state
    new_state = follow_way_succed(b, x0, y0, new_state)
    return ''.join(new_state)


def mutate_suffix(path, board):
    """
    Controles mutation by changing the suffix of path
    :param path:
    :param board:
    :return:
    """
    x, y = get_start(board)
    path_new = get_path_same_prefix(path, board)
    while not is_path_correct(x, y, path_new, board):
        path_new = get_path_same_prefix(path, board)
    return remove_constant_points(path_new)


def plot_graph(costs):
    """
    Graphs plot for costs
    :param costs:
    :return:
    """
    plt.figure()
    for i in range(len(np.array(costs).T)):
        plt.plot(np.array(costs)[:, i])
    plt.title("Costs")
    plt.show()


def read_data(filename):
    """
    Reads data from file
    :param filename:
    :return:
    """
    f = open(filename, "r")
    line = f.readline()
    t, n, m, s, population = line.split()
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
    return int(t), int(n), int(m), int(s), int(population), paths, np.array(board)


def get_start(board):
    """
    Find start position
    :param board:
    :return:
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 5:
                return int(j), int(i)


def get_millis(seconds):
    """
    seconds to millis converter
    :param seconds:
    :return:
    """
    return seconds * 10 ** 3


def get_current_time():
    """
    :return: current time
    """
    return get_millis(int(time.time()))


def get_min(paths_list):
    """
    Gets min path by len in path list
    :param paths_list:
    :return:
    """
    return min(paths_list, key=len)


def validate_indexes(i, j, path, limit):
    """
    Validates if indexes are != and there is a sens to swap
    on this indexes
    :param i:
    :param j:
    :param path:
    :param limit:
    :return:
    """
    while i == j or path[i] == path[j]:
        j = np.random.randint(0, limit)


def get_random_indexes(path):
    """Looses random indexes"""
    limit = len(path)
    i = np.random.randint(0, limit)
    j = np.random.randint(0, limit)
    validate_indexes(i, j, path, limit)
    return i, j


def swap(path):
    """Perform swap of steps in given string path"""
    path_list = list(path)
    i, j = get_random_indexes(path)
    path_list[j], path_list[i] = path_list[i], path_list[j]
    return ''.join(path_list)


def mutate_transposition(path, board):
    """Mutation by transposition swapping 2 random elements"""
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
    """
    Return closest blocks that agent can see
    :param x: cord1
    :param y: cord2
    :param board:
    :return:
    """
    return [get_left(x, y, board), get_upper(x, y, board), get_right(x, y, board), get_lower(x, y, board)]


def append_step(path, neighbours_list):
    """
    Function allows agent to take a look on the sides and if
    he can see the exit, he stays and return with side he has to went
    :param path:
    :param neighbours_list:
    :return:
    """
    index = neighbours_list.index(8)
    directions = ['L', 'U', 'R', 'D']
    return path + directions[index]


def is_path_correct(x, y, path, board):
    """
    Function check if path is correct by follwing it, if not
    returns " good path " = path til the wall
    :param x:
    :param y:
    :param path:
    :param board:
    :return:
    """
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
    """
    A little muttation before mutating
    swap to correct path ( transposition)
    :param path:
    :param board:
    :return:
    """
    x, y = get_start(board)
    new_path = swap(path)
    while not is_path_correct(x, y, new_path, board):
        new_path = swap(path)
    return new_path


def tournament_selection(population, board):
    """
    Provides something like races between parents, and choosing 2 best of them
    :param population:
    :param board:
    :return:
    """
    t = len(population)
    best = replace(np.random.choice(population), board)
    for _ in (1, t):
        beside = replace(np.random.choice(population), board)
        if len(beside) < len(best):
            best = beside
    return best, beside


def slides_selection(population):
    """
    Selection as on slides. We are computating it by quality/(all_qualities)sum
    And randomly selecting parents to  later crossover them.
    :param population:
    :return:
    """
    population = sorted(population, key=len)
    total_len = sum([len(pi) for pi in population])
    quality = [len(pi) / total_len for pi in population]
    result = [False for _ in range(len(population))]
    # random.shuffle(population)
    while result.count(True) < 2:
        for i in range(len(result)):
            if result.count(True) == 2:
                break
            if np.random.uniform(0, 1) < quality[i]:
                result[i] = True
    g = (i for i, e in enumerate(result) if e is True)
    i = next(g)
    j = next(g)
    return population[i], population[j]


def remove_constant_points(path):
    """
    remove constant points like "LR" from given path.
    :param path:
    :return:
    """
    z = path
    while "UD" in z or "DU" in z or "LR" in z or "RL" in z:
        z = z.replace("UD", "")
        z = z.replace("DU", "")
        z = z.replace("LR", "")
        z = z.replace("RL", "")
    return z


def cross_paths(path1, path2):
    """
    We are taking 4 indexes
    2 in path1 and 2 in path2.
    And we are swapping "middles" or sides.
    :param path1:
    :param path2:
    :return:
    """
    l1, l2 = len(path1), len(path2)
    c1, d1 = np.random.randint(0, l1 - 1), np.random.randint(0, l1 - 1)
    c2, d2 = np.random.randint(0, l2 - 1), np.random.randint(0, l2 - 1)
    if c1 > d1:
        c1, d1 = d1, c1
    if c2 > d2:
        c2, d2 = d2, c2
    return path1[:c1] + path2[c2:d2] + path1[d1:], path2[:c2] + path1[c1:d1] + path1[d2:]


def two_point_crossover(path1, path2, board, n, m):
    """
    Crossover of two given path
    :param path1:
    :param path2:
    :param board:
    :param n:
    :param m:
    :return:
    """
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


def genetic_algorithm_maze(t, n, m, s, p, paths, board, graphs=False, mutation=mutate_transposition,
                           selection=slides_selection):
    """
    :param t: time limitation
    :param n: board height
    :param m: board width
    :param s: quantity of initial solutions
    :param p: population quantity
    :param paths: initial solutions
    :param board: maze
    :param graphs: draw plots
    :param mutation: decide with function use to mixed_mutation
    :param selection: decide with function use to select parents
    :return:
    """
    end_time = get_millis(t) + get_current_time()
    population = paths

    if s < len(population):
        pass  # population.append(initial_solution(copy.deepcopy(board), get_start(board)))

    global_best = get_min(population)
    population_history = [[len(pi) for pi in population]]

    while get_current_time() <= end_time:
        best = get_min(population)
        Q = []
        for _ in range(int(s / 2)):
            Pa, Pb = selection(population)
            Ca, Cb = two_point_crossover(Pa, Pb, board, n, m)
            Q.append(mutation(Ca, board))
            Q.append(mutation(Cb, board))
            if len(best) < len(global_best):
                global_best = best
        population = Q
        population_history.append([len(pi) for pi in population])
    if graphs:
        plot_graph(population_history)
    return global_best, len(global_best)


def main():
    t, n, m, s, population, paths, board = read_data('tests/t2')
    # print(t, n, m, s, population)
    # print(paths)
    # for level in board:
    #    print(level)
    result = genetic_algorithm_maze(t, n, m, s, population, paths, board, graphs=True, mutation=mutate_suffix)
    print(result)


main()
