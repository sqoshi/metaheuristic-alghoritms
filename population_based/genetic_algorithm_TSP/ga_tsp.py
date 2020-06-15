import pprint
import random
import sys
import time

import matplotlib.pyplot as plt
import numpy as np


def rotate(A):
    B = []
    added = True
    while added:
        added = False
        col = []
        for row in A:
            try:
                col.append(row.pop(0))
            except IndexError:
                continue
            added = True
        col and B.append(col)
    return B


def plot_graph(arr):
    transposed_array = rotate(arr)
    if len(arr) > 2:
        for sub in transposed_array:
            plt.plot([i for i in range(len(sub))], sub, c=np.random.rand(3, ))
    else:
        plt.plot([i for i in range(len(transposed_array[1]))], transposed_array[1], c="red")
        plt.plot([i for i in range(len(transposed_array[0]))], transposed_array[0], c="blue")
    plt.show()


def read_data(filename):
    """
    Method read nxn matrix of distances, time and quantity of cities.
    :param filename: path to file
    :return:
    """
    f = open(filename, "r")
    line = f.readline()
    t, n = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line.split()])
        line = f.readline()
    return int(t), int(n), array


def get_next_city(graph, T):
    city = T[0]
    initial_min = 0
    row = graph[T[len(T) - 1]]
    for i in range(len(row)):
        if i not in T:
            if initial_min > row[i] or initial_min == 0:
                initial_min = row[i]
                city = i
    return city


def get_good_initial(graph, n, src):
    T = [src]
    for i in range(n):
        minimalCity = get_next_city(graph, T)
        T.append(minimalCity)
    return T[:len(T) - 1]


def get_current_time():
    return get_millis(int(time.time()))


def get_millis(t):
    return t * 1000


def swap(i, j, paths):
    path = paths.copy()
    path[i], path[j] = path[j], path[i]
    return path


def random_swap(path):
    i, j = random.sample([i for i in range(len(path))], 2)
    return swap(i, j, path)


def compute_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i + 1]]
    return total_distance


def get_random_population(n, pop_size):
    num_list = [i for i in range(n)]
    pop = [num_list.copy() for _ in range(pop_size)]
    for x in pop:
        random.shuffle(x)
    return pop


def evaluate(path, distances):
    return 1 / (compute_distance(path, distances) + distances[path[len(path) - 1]][path[0]])


def get_min(population, distances):
    best = random.choice(population)
    for x in population:
        if compute_distance(x, distances) < compute_distance(best, distances):
            best = x
    return best


def cycle_crossover(p1, p2, prc):
    for i in range(len(p1)):
        if random.uniform(0, 1) < prc:
            p1[p1.index(p2[i])], p2[p2.index(p1[i])] = p1[i], p2[i]
            p1[i], p2[i] = p2[i], p1[i]
    return p1, p2


def tournament_selection(population, distances):
    ts = 3
    best = random.choice(population)
    for i in range(0, ts):
        nex = random.choice(population)
        if compute_distance(nex, distances) < compute_distance(best, distances):
            best = nex
    return best


def get_locus(population, i):
    locus = []
    for x in population:
        locus += [x[i]]
    return locus


def improve_and_reproduce(population, pop_size, distances):
    selected = []
    popu = population.copy()
    while len(selected) < pop_size // 3:
        z = get_min(popu, distances)
        selected.append(z)
        popu.remove(z)
    while len(selected) < pop_size:
        z = random.choice(popu)
        selected.append(z)
        popu.remove(z)
    return selected


def hard_mutate(path):
    i, j = random.sample([i for i in range(len(path))], 2)
    s, b = i, j
    if j < i:
        s, b = j, i
    return path[s:b] + path[:s] + path[b:]


def genetic_algorithm(t, n, distances, pop_size=24, plot=True, prcx=0.5):
    his = []
    end_time = get_current_time() + get_millis(t)
    population = get_random_population(n, pop_size)
    population.append(get_good_initial(distances, n, random.randint(0, n - 1)))
    best = get_min(population, distances)
    while get_current_time() <= end_time:
        Q = []
        while len(Q) < pop_size:
            p1 = tournament_selection(population, distances)
            p2 = tournament_selection(population, distances)
            c1, c2 = cycle_crossover(p1, p2, prcx)
            c1 = random_swap(c1)
            c2 = random_swap(c2)
            if c1 not in population:
                Q.append(c1)
            if c2 not in population:
                Q.append(c2)
        population.extend(Q)
        population.append(get_good_initial(distances, n, random.randint(0, n - 1)))
        population = improve_and_reproduce(population, pop_size, distances)
        opponent = get_min(population, distances).copy()
        if compute_distance(opponent, distances) < compute_distance(best, distances):
            best = opponent
        if plot:
            his.append([compute_distance(best, distances),
                        compute_distance(opponent, distances)])  # [compute_distance(x, distances) for x in population])
    if plot:
        plot_graph(his)
    return best


def test():
    arr = [[1, 2, 3], [4, 5, 6]]
    loc = get_locus(arr, 2)
    loc[0], loc[1] = loc[1], loc[0]
    print(arr)


def main(filename):
    t, n, a = read_data(filename)
    pprint.pprint(np.matrix(a))
    z = genetic_algorithm(3, n, a)
    print(z, compute_distance(z, a))


## przyjmuje input w formacie jak w zadaniu 2 na liscie nr 1 (alg meta 15 czerwca 2020)
main(sys.argv[1])
